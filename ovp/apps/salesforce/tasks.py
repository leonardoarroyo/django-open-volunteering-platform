from simple_salesforce import Salesforce
from celery import task
from django.conf import settings
from ovp.apps.organizations.models import Organization

def get_auth_data(channel):
    integration_data = getattr(settings, 'SALESFORCE_INTEGRATION', {})
    channel_integration = integration_data.get(channel, None)
    return {
        "username": channel_integration["username"],
        "password": channel_integration["password"],
        "security_token": channel_integration["security_token"],
        "domain": channel_integration.get("domain", "test"),
    }

def get_organization_dict(organization):
    return {
        "Name": organization.name,
        "New_CNPJ__c": organization.document.strip().replace(".", "").replace("/", "").replace("-", "") if organization.document else "",
        "Description": organization.details,
        "New_Descricao_Reduzida__c": organization.description,
        "Website": organization.website,
        "New_Instagram__c": organization.instagram_user,
        "New_Facebook__c": organization.facebook_page,
        "New_Blog__c": f"https://atados.com.br/ong/{ organization.slug }",
        "uid__c": organization.id,
        "BillingCountry": organization.address.address_dict()['country']['long_name'] if organization.address else None,
        "BillingStreet": organization.address.address_line if organization.address else None
    }

def create_organization(sf, organization):
    return sf.Account.create(get_organization_dict(organization))

def update_organization(sf, existing_id, organization):
    return sf.Account.update(existing_id, get_organization_dict(organization))

def create_contacts(sf, organization, id):
    return [
        sf.Contact.create({
            "LastName": organization.contact_name or "Vazio",
            "Phone": organization.contact_phone,
            "Email": organization.contact_email,
            "AccountId": id
        }),
        sf.Contact.create({
            "LastName": organization.owner.name or "Vazio",
            "Phone": organization.owner.phone,
            "Email": organization.owner.email,
            "AccountId": id
        })
    ]

def get_organization_id(sf, organization):
    # Try first salesforce_id
    if organization.salesforce_id:
        return organization.salesforce_id

    # Then uid
    res = sf.query(f'SELECT Id FROM Account WHERE uid__c = { organization.pk }')

    if not len(res['records']):
        return None

    return res['records'][0]['Id']

def create_client(channel):
    auth_data = get_auth_data(channel)
    return Salesforce(**auth_data)

@task(name='ovp.apps.salesforce.push_organization')
def push_organization(organization_pk):
    organization = Organization.objects.get(pk=organization_pk)
    sf = create_client(organization.channel.slug)

    existing_id = get_organization_id(sf, organization)
    if existing_id:
        sf_org = update_organization(sf, existing_id, organization)
    else:
        sf_org = create_organization(sf, organization)
        create_contacts(sf, organization, sf_org["id"])
