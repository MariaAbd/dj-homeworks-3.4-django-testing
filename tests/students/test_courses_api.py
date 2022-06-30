import pytest as pytest
from model_bakery import baker
from rest_framework.test import APIClient

from students.models import Course, Student


@pytest.fixture()
def client():
    return APIClient()


@pytest.fixture()
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture()
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_list_courses(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get('/courses/')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(_quantity=5)
    response = client.get('/courses/')
    data = response.json()

    assert response.status_code == 200
    for i, c in enumerate(data):
        assert c['id'] == courses[i].id


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/courses/', data={'name': 'course_1'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    course_factory = course_factory(_quantity=10)
    filter_id = Course.objects.filter(id=course_factory[0].id)
    response = client.get('/courses/')
    data = response.json()

    assert response.status_code == 200
    for c in filter_id:
        assert data[0]['id'] == c.id


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    course_factory = course_factory(_quantity=10)
    filter_name = Course.objects.filter(name=course_factory[2].name)
    response = client.get('/courses/')
    data = response.json()

    assert response.status_code == 200
    assert data[2]['name'] == filter_name[0].name


@pytest.mark.django_db
def test_update_course(client):
    course = Course.objects.create(name='course')
    updated_course = Course.objects.filter(id=course.id)
    updated_course.update(name='test_course')
    response = client.get('/courses/')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == updated_course[0].name


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=10)

    deleted_course = Course.objects.filter(id=course[1].id)
    deleted_course.delete()
    response = client.get('/courses/34/')
    data = response.json()

    assert response.status_code == 404
    assert course[1].id not in data










