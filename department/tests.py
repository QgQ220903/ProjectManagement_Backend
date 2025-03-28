from django.test import TestCase
from .models import Department
# Create your tests here.
class DepartmentTestCase(TestCase):
  def setUp(self):
    department1 = Department(name="Nhân Sự", description="Phòng chịu trách nhiệm về quản lý nhân sự và tuyển dụng.")
    department2 = Department(name="Tài chính", description="Phòng chịu trách nhiệm về quản lý tài chính và kế toán.")

    