from django.test import TestCase

from django.core.cache import cache

from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from ovp.apps.projects.models import Project
from ovp.apps.users.models import User
from ovp.apps.organizations.models import Organization

from ovp.apps.channels.models.channel_setting import ChannelSetting

from collections import OrderedDict

import copy


base_project = {"name": "test project", "slug": "test-cant-override-slug-on-creation", "details": "this is just a test project", "description": "the project is being tested", "minimum_age": 18, "address": {"typed_address": "r. tecainda, 81, sao paulo"}, "disponibility": {"type": "work", "work": {"description": "abc"}}, "causes": [{"id": 1}, {"id": 2}], "skills": [{"id": 3}, {"id": 4}]}

class ProjectResourceViewSetTestCase(TestCase):
  def setUp(self):
    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION", value="1", object_channel="default")
    cache.clear()

  def test_cant_create_project_unauthenticated(self):
    """Assert that it's not possible to create a project while unauthenticated"""
    client = APIClient()
    response = client.post(reverse("project-list"), {}, format="json")

    self.assertTrue(response.data["detail"] == "Authentication credentials were not provided.")
    self.assertTrue(response.status_code == 401)

  def test_can_create_project(self):
    """Assert that it's possible to create a project while authenticated"""
    user = User.objects.create_user(email="test_can_create_project@gmail.com", password="testcancreate", object_channel="default")

    data = copy.copy(base_project)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post(reverse("project-list"), data, format="json")

    self.assertTrue(response.status_code == 201)
    self.assertTrue(response.data["id"])
    self.assertTrue(response.data["name"] == data["name"])
    self.assertTrue(response.data["slug"] == "test-project")
    self.assertTrue(response.data["details"] == data["details"])
    self.assertTrue(response.data["description"] == data["description"])
    self.assertTrue(response.data["minimum_age"] == data["minimum_age"])
    self.assertTrue(len(response.data["causes"]) == 2)
    self.assertTrue(len(response.data["skills"]) == 2)

    project = Project.objects.get(pk=response.data["id"])
    self.assertTrue(project.owner.id == user.id)
    self.assertTrue(project.address.typed_address == data["address"]["typed_address"])


  def test_cant_create_project_empty_name(self):
    """Assert that it's not possible to create a project with empty name"""
    user = User.objects.create_user(email="test_can_create_project@gmail.com", password="testcancreate", object_channel="default")

    client = APIClient()
    client.force_authenticate(user=user)

    data = copy.copy(base_project)
    data["name"] = ""

    response = client.post(reverse("project-list"), data, format="json")
    self.assertTrue(response.data["name"][0] == "This field may not be blank.")


  def test_project_retrieval(self):
    """Assert projects can be retrieved"""
    user = User.objects.create_user(email="test_retrieval@gmail.com", password="testretrieval", object_channel="default")

    client = APIClient()
    client.force_authenticate(user=user)

    data = copy.copy(base_project)
    response = client.post(reverse("project-list"), data, format="json")

    response = client.get(reverse("project-detail", ["test-project"]), format="json")

    self.assertTrue(response.data["name"] == data["name"])
    self.assertTrue(response.data["slug"] == "test-project")
    self.assertTrue(response.data["details"] == data["details"])
    self.assertTrue(response.data["description"] == data["description"])
    self.assertTrue(response.data["published"] == False)
    self.assertTrue(type(response.data["owner"]) in [dict, OrderedDict])
    self.assertTrue(type(response.data["applies"]) is list)
    self.assertTrue(type(response.data["applied_count"]) is int)
    self.assertTrue(type(response.data["max_applies_from_roles"]) is int)
    self.assertTrue(len(response.data["causes"]) == 2)
    self.assertTrue(len(response.data["skills"]) == 2)



class ProjectCloseTestCase(TestCase):
  def setUp(self):
    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION", value="1", object_channel="default")
    cache.clear()

    user = User.objects.create_user(email="test_close@gmail.com", password="testclose", object_channel="default")
    self.client = APIClient()
    self.client.force_authenticate(user=user)

    data = copy.copy(base_project)
    self.project = self.client.post(reverse("project-list"), data, format="json")

  def test_cant_close_project_if_not_owner_or_organization_member(self):
    """ Assert that it's not possible to close a project if not the owner or organization member """
    user = User.objects.create_user(email="otheruser@gmail.com", password="otheruser", object_channel="default")
    self.client.force_authenticate(user=user)
    response = self.client.post(reverse("project-close", ["test-project"]), format="json")
    self.assertTrue(response.status_code == 403)


  def test_can_close_project(self):
    """ Assert that it's possible to close a project """
    response = self.client.post(reverse("project-close", ["test-project"]), format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["closed"] == True)
    self.assertTrue(response.data["closed"])


class ProjectCommentTestCase(TestCase):
  def setUp(self):
    user = User.objects.create_user(email="test_comment@gmail.com", password="testcomment", object_channel="default")
    self.client = APIClient()
    self.client.force_authenticate(user=user)

    data = copy.copy(base_project)
    self.project = self.client.post(reverse("project-list"), data, format="json")

    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION", value="1", object_channel="default")
    cache.clear()

  def test_user_can_comment_in_project(self):
    """ Assert that user can comment in project """
    comment = {
      "content": "test comment",
    }
    response = self.client.post(reverse("project-commentary", ["test-project"]), comment, format="json")
    self.assertTrue(response.status_code == 200)


class ProjectWithOrganizationTestCase(TestCase):
  def setUp(self):
    cache.clear()

    self.user = User.objects.create_user(email="test_can_create_project@gmail.com", password="testcancreate", object_channel="default")
    self.second_user = User.objects.create_user(email="test_second_user@test.com", password="testcancreate", object_channel="default")
    self.third_user = User.objects.create_user(email="test_third_user@test.com", password="testcancreate", object_channel="default")
    self.data = copy.copy(base_project)
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

  def test_no_organization(self):
    """Test no organization returns error"""
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["organization"] == ["This field is required."])
    self.assertTrue(response.status_code == 400)

  def test_organization_is_int(self):
    """Test organization field must be int"""
    self.data['organization_id'] = 'str'

    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["organization_id"] == ["A valid integer is required."])
    self.assertTrue(response.status_code == 400)

  def test_user_is_owner_or_member(self):
    """Test user is owner or member of organization"""
    wrong_org = Organization(name="test", type=0, owner=self.second_user)
    wrong_org.save(object_channel="default")

    self.data['organization_id'] = wrong_org.pk
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.status_code == 403)

  def test_can_create_in_any_organization_if_settings_allow(self):
    """Test user can create project inside any organization if properly configured"""
    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_IN_ANY_ORGANIZATION", value="1", object_channel="default")
    cache.clear()

    wrong_org = Organization(name="test", type=0, owner=self.second_user)
    wrong_org.save(object_channel="default")

    self.data['organization_id'] = wrong_org.pk
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.status_code == 201)

  def test_can_create(self):
    """Test user can create project with valid organization"""
    organization = Organization(name="test", type=0, owner=self.user)
    organization.save(object_channel="default")
    organization.members.add(self.second_user)

    self.data['organization_id'] = organization.pk
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.status_code == 201)

    self.client.force_authenticate(self.second_user)
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.status_code == 201)

  def test_can_hide_address(self):
    """Test user can create project with valid organization"""
    org = Organization(name="test", type=0, owner=self.user)
    org.save(object_channel="default")
    org.members.add(self.second_user)

    self.data['organization_id'] = org.pk
    self.data['hidden_address'] = True
    response = self.client.post(reverse("project-list"), self.data, format="json")

    # Owner retrieving
    response = self.client.get(reverse("project-detail", ["test-project"]), format="json")
    self.assertTrue(response.data["address"]["typed_address"] == self.data["address"]["typed_address"])
    self.assertTrue(response.data["hidden_address"] == True)

    # Organization member retrieving
    self.client.force_authenticate(self.second_user)
    response = self.client.get(reverse("project-detail", ["test-project"]), format="json")
    self.assertTrue(response.data["address"]["typed_address"] == self.data["address"]["typed_address"])
    self.assertTrue(response.data["hidden_address"] == True)

    # Non member retrieving
    self.client.force_authenticate(self.third_user)
    response = self.client.get(reverse("project-detail", ["test-project"]), format="json")
    self.assertTrue(response.data["address"] == None)
    self.assertTrue(response.data["hidden_address"] == True)

    # Project without organization
    self.client.force_authenticate(self.second_user)
    Project.objects.filter(slug="test-project").update(organization = None)
    response = self.client.get(reverse("project-detail", ["test-project"]), format="json")
    self.assertTrue(response.data["address"] == None)
    self.assertTrue(response.data["hidden_address"] == True)


class ManageableProjectsRouteTestCase(TestCase):
  def setUp(self):
    self.user = User.objects.create_user(email="test_can_create_project@gmail.com", password="testcancreate", object_channel="default")
    self.user2 = User.objects.create_user(email="test_can_create_project2@gmail.com", password="testcancreate", object_channel="default")
    self.organization = Organization(name="test", type=0, owner=self.user)
    self.organization.save(object_channel="default")
    self.organization2 = Organization(name="test2", type=0, owner=self.user2)
    self.organization2.save(object_channel="default")
    self.organization2.members.add(self.user)

    p = Project.objects.create(name="test project 1", owner=self.user, object_channel="default")
    p = Project.objects.create(name="test project 2", owner=self.user, organization=self.organization, object_channel="default")
    p = Project.objects.create(name="test project 3", owner=self.user2, organization=self.organization2, object_channel="default")

    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

  def test_requires_authentication(self):
    """Test hitting route unauthenticated returns 401"""
    client = APIClient()
    response = client.get(reverse("project-manageable"), {}, format="json")
    self.assertTrue(response.status_code == 401)


  def test_returns_projects(self):
    """Test hitting route authenticated returns projects"""
    response = self.client.get(reverse("project-manageable"), {}, format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(len(response.data) == 3)


class ProjectResourceUpdateTestCase(TestCase):
  def setUp(self):
    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION", value="1", object_channel="default")
    cache.clear()

    self.user = User.objects.create_user(email="test_can_create_project@gmail.com", password="testcancreate", object_channel="default")
    self.data = copy.copy(base_project)
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.status_code == 201)

  def test_wrong_user_cant_update(self):
    """Test only owner can update project"""
    wrong_user = User.objects.create_user(email="wrong_user@gmail.com", password="testcancreate", object_channel="default")
    wrong_user.save()
    self.client.force_authenticate(user=wrong_user)

    response = self.client.patch(reverse("project-detail", ["test-project"]), {}, format="json")
    self.assertTrue(response.status_code == 403)

  def test_update_fields(self):
    """Test patch request update fields"""
    updated_project = {"name": "test update", "details": "update", "description": "update", "causes": [{"id": 3}], "skills": [{"id": 1}, {"id": 2}, {"id": 3}]}
    response = self.client.patch(reverse("project-detail", ["test-project"]), updated_project, format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["name"] == "test update")
    self.assertTrue(response.data["details"] == "update")
    self.assertTrue(response.data["description"] == "update")
    self.assertTrue(len(response.data["causes"]) == 1)
    self.assertTrue(len(response.data["skills"]) == 3)

    user = User.objects.create_user(email="another@user.com", password="testcancreate", object_channel="default")
    organization = Organization(name="test", type=0, owner=self.user)
    organization.save(object_channel="default")
    organization.members.add(user)
    project = Project.objects.get(pk=response.data['id'])
    project.organization = organization
    project.save()
    self.client.force_authenticate(user)
    response = self.client.patch(reverse("project-detail", ["test-project"]), updated_project, format="json")
    self.assertTrue(response.status_code == 200)

  def test_update_address(self):
    """Test patch request update address resource"""
    updated_project = {"address": {"typed_address": "r. capote valente, 701, sao paulo"}}
    response = self.client.patch(reverse("project-detail", ["test-project"]), updated_project, format="json")

    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["address"]["typed_address"] == "r. capote valente, 701, sao paulo")

  def test_update_disponibility(self):
    """Test patch request update disponibility resource"""
    updated_project = {"disponibility": {"type": "job", "job": {"dates": [{"name": "update", "start_date": "2013-01-29T12:34:56.123Z", "end_date": "2013-01-29T13:34:56.123Z"}, {"name": "test1", "start_date": "2013-02-01T12:34:56.123Z", "end_date": "2013-02-01T13:34:56.123Z"}]}}}
    response = self.client.patch(reverse("project-detail", ["test-project"]), updated_project, format="json")

    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["disponibility"]["type"] == "job")
    self.assertTrue(response.data["disponibility"]["job"]["dates"][0]["name"] == "update")

    updated_project = {"disponibility": {"type": "work", "work": {"description": "update"}}}
    response = self.client.patch(reverse("project-detail", ["test-project"]), updated_project, format="json")

    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["disponibility"]["type"] == "work")
    self.assertTrue(response.data["disponibility"]["work"]["description"] == "update")

  def test_update_roles(self):
    """Test patch request update roles resource"""
    expected_response = [{"name": "test", "prerequisites": "test2", "details": "test3", "vacancies": 5, "applied_count": 0, "id": 1}]
    updated_project = {"roles": [{"name": "test", "prerequisites": "test2", "details": "test3", "vacancies": 5}]}
    response = self.client.patch(reverse("project-detail", ["test-project"]), updated_project, format="json")

    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["roles"] == expected_response)


class DisponibilityTestCase(TestCase):
  def setUp(self):
    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION", value="1", object_channel="default")
    cache.clear()

    self.user = User.objects.create_user(email="test_can_create_project@gmail.com", password="testcancreate", object_channel="default")
    self.data = copy.copy(base_project)
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)

  def test_no_disponibility(self):
    """Test no disponibility returns error"""
    del self.data["disponibility"]
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"] == ["This field is required."])
    self.assertTrue(response.status_code == 400)

  def test_disponibility_type_required(self):
    """Test disponibility type is required"""
    self.data["disponibility"] = {}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["type"] == ["This field is required."])
    self.assertTrue(response.status_code == 400)

  def test_type_not_work_or_job(self):
    """Test disponibility type can't be different than work or job"""
    self.data["disponibility"] = {"type": "test"}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["type"] == ["Must have either be 'work' or 'job'."])
    self.assertTrue(response.status_code == 400)

  def test_empty_job_or_work(self):
    """Test empty job or work returns error"""
    self.data["disponibility"] = {"type": "job"}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["job"] == ["This field is required if type=\"job\"."])
    self.assertTrue(response.status_code == 400)

    self.data["disponibility"] = {"type": "work"}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["work"] == ["This field is required if type=\"work\"."])
    self.assertTrue(response.status_code == 400)

 # def test_work_description_required(self):
 #   """Test work description is required"""
 #   self.data["disponibility"] = {"type": "work", "work": {}}
 #   response = self.client.post(reverse("project-list"), self.data, format="json")
 #   self.assertTrue(response.data["disponibility"]["work"]["description"] == ["This field is required."])
 #   self.assertTrue(response.status_code == 400)

  def test_correct_work(self):
    """Test correct work returns success"""
    self.data["disponibility"] = {"type": "work", "work": {"description": "test desc", "weekly_hours": 6}}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["type"] == "work")
    self.assertTrue(response.data["disponibility"]["work"]["description"] == "test desc")
    self.assertTrue(response.data["disponibility"]["work"]["weekly_hours"] == 6)
    self.assertTrue(response.status_code == 201)

  def test_job_dates_required(self):
    """Test job dates is required"""
    self.data["disponibility"] = {"type": "job", "job": {}}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["job"]["dates"] == ["This field is required."])
    self.assertTrue(response.status_code == 400)

  def test_job_dates_cant_be_empty(self):
    """Test job dates can't be empty"""
    self.data["disponibility"] = {"type": "job", "job": {"dates": []}}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["job"]["dates"] == ["Must have at least one date."])
    self.assertTrue(response.status_code == 400)

  def test_job_dates_cant_be_wrong_type(self):
    """Test job dates can't be wrong type"""
    self.data["disponibility"] = {"type": "job", "job": {"dates": ''}}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["job"]["dates"]["non_field_errors"] == ["Expected a list of items but got type \"str\"."])
    self.assertTrue(response.status_code == 400)

  def test_job_dates_cant_have_bad_formatted_date(self):
    """Test job dates can't have bad formatted date"""
    self.data["disponibility"] = {"type": "job", "job": {"dates": [{"start_date": "abc", "end_date": "abc"}]}}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["disponibility"]["job"]["dates"][0]["start_date"] == ["Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."])
    self.assertTrue(response.data["disponibility"]["job"]["dates"][0]["end_date"] == ["Datetime has wrong format. Use one of these formats instead: YYYY-MM-DDThh:mm[:ss[.uuuuuu]][+HH:MM|-HH:MM|Z]."])
    self.assertTrue(response.status_code == 400)

  def test_job_returns_success(self):
    """Test correct job returns success"""
    self.data["disponibility"] = {"type": "job", "job": {"dates": [{"name": "test1", "start_date": "2013-01-29T12:34:56.123Z", "end_date": "2013-01-29T13:34:56.123Z"}, {"name": "test1", "start_date": "2013-02-01T12:34:56.123Z", "end_date": "2013-02-01T13:34:56.123Z"}]}}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.status_code == 201)
    self.assertTrue(response.data["disponibility"]["job"]["dates"][0]["start_date"] == "2013-01-29T12:34:56.123000Z")
    self.assertTrue(response.data["disponibility"]["job"]["dates"][0]["end_date"] == "2013-01-29T13:34:56.123000Z")
    self.assertTrue(response.data["disponibility"]["job"]["dates"][1]["start_date"] == "2013-02-01T12:34:56.123000Z")
    self.assertTrue(response.data["disponibility"]["job"]["dates"][1]["end_date"] == "2013-02-01T13:34:56.123000Z")

    self.assertTrue(response.data["disponibility"]["job"]["start_date"] == "2013-01-29T12:34:56.123000Z")
    self.assertTrue(response.data["disponibility"]["job"]["end_date"] == "2013-02-01T13:34:56.123000Z")



class VolunteerRoleTestCase(TestCase):
  def setUp(self):
    ChannelSetting.objects.create(key="CAN_CREATE_PROJECTS_WITHOUT_ORGANIZATION", value="1", object_channel="default")
    cache.clear()

    self.user = User.objects.create_user(email="test_can_create_project@gmail.com", password="testcancreate", object_channel="default")
    self.data = copy.copy(base_project)
    self.client = APIClient()
    self.client.force_authenticate(user=self.user)


  def test_roles_is_correct_type(self):
    """Test roles is correct type"""
    self.data["roles"] = {"name": "test", "prerequisites": "test2", "details": "test3", "vacancies": 5}
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.data["roles"]["non_field_errors"] == ["Expected a list of items but got type \"dict\"."])
    self.assertTrue(response.status_code == 400)


  def test_roles_get_saved(self):
    """Test roles get saved"""
    expected_response = [{"name": "test", "prerequisites": "test2", "details": "test3", "vacancies": 5, "applied_count": 0, "id": 1}]
    self.data["roles"] = [{"name": "test", "prerequisites": "test2", "details": "test3", "vacancies": 5}]
    response = self.client.post(reverse("project-list"), self.data, format="json")
    self.assertTrue(response.status_code == 201)
    self.assertTrue(response.data["roles"] == expected_response)

    response = self.client.get(reverse("project-detail", ['test-project']), format="json")
    self.assertTrue(response.status_code == 200)
    self.assertTrue(response.data["roles"] == expected_response)
