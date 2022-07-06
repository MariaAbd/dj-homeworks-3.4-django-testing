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
    response = client.get('/api/v1/courses/')
    data = response.json()

    assert response.status_code == 200
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_get_course(client, course_factory):
    courses = course_factory(name='course')
    response = client.get(f'/api/v1/courses/{courses.id}/')
    data = response.json()
    course = Course.objects.filter(id=data['id'])

    assert response.status_code == 200
    assert data['id'] == course[0].id


@pytest.mark.django_db
def test_create_course(client):
    count = Course.objects.count()
    response = client.post('/api/v1/courses/', data={'name': 'course_1'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1


@pytest.mark.django_db
def test_filter_course_id(client, course_factory):
    course_factory = course_factory(_quantity=10)
    print(course_factory[0].id)
    filter_id = Course.objects.filter(id=course_factory[0].id)
    response = client.get(f'/api/v1/courses/?id={course_factory[0].id}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['id'] == filter_id[0].id


@pytest.mark.django_db
def test_filter_course_name(client, course_factory):
    course_factory = course_factory(_quantity=10)
    filter_name = Course.objects.filter(name=course_factory[2].name)
    response = client.get(f'/api/v1/courses/?name={course_factory[2].name}')
    data = response.json()

    assert response.status_code == 200
    assert data[0]['name'] == filter_name[0].name


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(name='course_1')
    client.delete(f'/api/v1/courses/?name={course.id}')
    response = client.get(f'/api/v1/courses/?name={course.id}')
    data = response.json()

    assert response.status_code == 200
    assert course.id not in data


@pytest.mark.django_db
def test_update_course(client, course_factory):
    course = course_factory(name='course')
    print(course.name)
    print(course.id)
    u_c = client.put(f'/api/v1/courses/?id={course.id}',
                     data={'name': 'updated_course', 'students': ['1', '2']},
                     format='json',
                     )

    response = client.get(f'/api/v1/courses/?id={course.id}')
    data = response.json()
    for d in data:
        print(d.items())

    assert response.status_code == 200
    assert data[0]['name'] != course.name
