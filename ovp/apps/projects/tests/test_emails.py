from django.test import TestCase
from django.core import mail

from ovp.apps.core.helpers import get_email_subject, is_email_enabled
from ovp.apps.users.models import User
from ovp.apps.projects.models import Project, Apply
from ovp.apps.core.models import Commentary

class TestEmailTriggers(TestCase):
  def test_project_creation_trigger_email(self):
    """Assert that email is triggered when creating a project"""
    user = User.objects.create_user(email="test_project@project.com", password="test_project", object_channel="default")
    mail.outbox = [] # Mails sent before creating don't matter
    project = Project.objects.create(name="test project", slug="test project", details="abc", description="abc", owner=user, object_channel="default")


    if is_email_enabled("default", "projectCreated"):
      self.assertTrue(len(mail.outbox) == 1)
      self.assertTrue(mail.outbox[0].subject == get_email_subject("default", "projectCreated", "Project created"))
    else: # pragma: no cover
      self.assertTrue(len(mail.outbox) == 0)

  def test_project_publishing_trigger_email(self):
    """Assert that email is triggered when publishing a project"""
    user = User.objects.create_user(email="test_project@project.com", password="test_project", object_channel="default")
    project = Project.objects.create(name="test project", slug="test project", details="abc", description="abc", owner=user, object_channel="default")

    mail.outbox = [] # Mails sent before publishing don't matter
    project.published = True
    project.save()

    if is_email_enabled("default", "projectPublished"): # pragma: no cover
      self.assertTrue(len(mail.outbox) == 1)
      self.assertTrue(mail.outbox[0].subject == get_email_subject("default", "projectPublished", "Project published"))
    else: # pragma: no cover
      self.assertTrue(len(mail.outbox) == 0)


  def test_project_closing_trigger_email(self):
    """Assert that email is triggered when closing a project"""
    user = User.objects.create_user(email="test_project@project.com", password="test_project", object_channel="default")
    project = Project.objects.create(name="test project", slug="test project", details="abc", description="abc", owner=user, object_channel="default")

    mail.outbox = [] # Mails sent before closing don't matter
    project.closed = True
    project.save()


    if is_email_enabled("default", "projectClosed"): # pragma: no cover
      self.assertTrue(len(mail.outbox) == 1)
      self.assertTrue(mail.outbox[0].subject == get_email_subject("default", "projectClosed", "Project closed"))
    else: # pragma: no cover
      self.assertTrue(len(mail.outbox) == 0)


  def test_apply_trigger_email(self):
    """Assert that applying to project trigger one email to volunteer and one to project owner"""
    user = User.objects.create_user(email="test_project@project.com", password="test_project", object_channel="default")
    volunteer = User.objects.create_user(email="test_volunteer@project.com", password="test_volunteer", object_channel="default")
    project = Project.objects.create(name="test project", slug="test project", details="abc", description="abc", owner=user, object_channel="default")

    mail.outbox = [] # Mails sent before applying don't matter
    apply = Apply(project=project, user=volunteer, email=volunteer.email)
    apply.save(object_channel="default")

    recipients = [x.to[0] for x in mail.outbox]
    subjects = [x.subject for x in mail.outbox]

    if is_email_enabled("default", "volunteerApplied-ToVolunteer"): # pragma: no cover
      self.assertTrue(get_email_subject("default", "volunteerApplied-ToVolunteer", "Applied to project") in subjects)
      self.assertTrue("test_project@project.com" in recipients)

    if is_email_enabled("default", "volunteerApplied-ToOwner"): # pragma: no cover
      self.assertTrue(get_email_subject("default", "volunteerApplied-ToOwner", "New volunteer") in subjects)
      self.assertTrue("test_volunteer@project.com" in recipients)


  def test_unapply_trigger_email(self):
    """Assert that applying to project trigger one email to volunteer and one to project owner"""
    user = User.objects.create_user(email="test_project@project.com", password="test_project", object_channel="default")
    volunteer = User.objects.create_user(email="test_volunteer@project.com", password="test_volunteer", object_channel="default")
    project = Project.objects.create(name="test project", slug="test project", details="abc", description="abc", owner=user, object_channel="default")

    mail.outbox = [] # Mails sent before applying don't matter
    apply = Apply(project=project, user=volunteer, email=volunteer.email)
    apply.save(object_channel="default")
    apply.status = "unapplied"
    apply.save()

    recipients = [x.to[0] for x in mail.outbox]
    subjects = [x.subject for x in mail.outbox]

    if is_email_enabled("default", "volunteerUnapplied-ToVolunteer"): # pragma: no cover
      self.assertTrue(get_email_subject("default", "volunteerUnapplied-ToVolunteer", "Unapplied from project") in subjects)
      self.assertTrue("test_project@project.com" in recipients)

    if is_email_enabled("default", "volunteerUnapplied-ToOwner"): # pragma: no cover
      self.assertTrue(get_email_subject("default", "volunteerUnapplied-ToOwner", "Volunteer unapplied from project") in subjects)
      self.assertTrue("test_volunteer@project.com" in recipients)


 # def test_comment_project_trigger_email(self):
 #   """Assert that email is triggered when user comment in project"""
 #   user = User.objects.create_user(email="test_project@project.com", password="test_project", object_channel="default")
 #   project = Project(name="test project", slug="test project", details="abc", description="abc", owner=user)
 #   project.save(object_channel="default")

 #   mail.outbox = [] # Mails sent before publishing don't matter
 #   comment = Commentary(content="test message", user=user)
 #   comment.save(object_channel="default")

 #   if is_email_enabled("sendComment"): # pragma: no cover
 #     self.assertTrue(len(mail.outbox) == 1)
 #     self.assertTrue(mail.outbox[0].subject == get_email_subject("sendComment", "You received a comment"))
 #   else: # pragma: no cover
 #     self.assertTrue(len(mail.outbox) == 0)


 # def test_comment_reply__project_trigger_email(self):
 #   """Assert that email is triggered when user reply another comment in project"""
 #   user = User.objects.create_user(email="test_project@project.com", password="test_project", object_channel="default")
 #   project = Project(name="test project", slug="test project", details="abc", description="abc", owner=user)
 #   project.save(object_channel="default")

 #   parent_comment = Commentary(content="test message 1", user=user)
 #   parent_comment.save(object_channel="default")

 #   mail.outbox = [] # Mails sent before publishing don't matter
 #   comment = Commentary(content="test message 2", reply_to=parent_comment, user=user)
 #   comment.save(object_channel="default")

 #   if is_email_enabled("commentReply"): # pragma: no cover
 #     self.assertTrue(len(mail.outbox) == 1)
 #     self.assertTrue(mail.outbox[0].subject == get_email_subject("commentReply", "Your comment was replied"))
 #   else: # pragma: no cover
 #     self.assertTrue(len(mail.outbox) == 0)
