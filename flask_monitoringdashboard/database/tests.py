"""
Contains all functions that returns results of all tests
"""
from sqlalchemy import func
from sqlalchemy.orm import joinedload

from flask_monitoringdashboard.database import Endpoint, Test, TestResult, TestEndpoint


def add_or_update_test(db_session, name, passing, last_tested, version_added, time_added):
    """ Add a unit test or update it. """
    test = db_session.query(Test).filter(Test.name == name).first()
    if test:
        test.name = name
        test.passing = passing
        test.last_tested = last_tested
        test.version_added = version_added
        test.time_added = time_added
    else:
        db_session.add(Test(name=name, passing=passing, last_tested=last_tested, version_added=version_added,
                            time_added=time_added))
    db_session.commit()


def add_test_result(db_session, name, exec_time, time, version, job_id, iteration):
    """ Add a test result to the database. """
    test_id = db_session.query(Test.id).filter(Test.name == name).first().id
    db_session.add(TestResult(test_id=test_id, execution_time=exec_time, time_added=time, app_version=version,
                              travis_job_id=job_id, run_nr=iteration))


def get_sorted_job_ids(db_session, column, limit):
    """ Returns a decreasing sorted list of the Travis job ids. """
    query = db_session.query(column).group_by(column)
    if limit:
        query = query.limit(limit)
    return sorted([int(float(build[0])) for build in query.all()], reverse=True)


def get_test_suites(db_session, limit=None):
    """ Returns a decreasing sorted list of Travis job ids that collected Test data. """
    return get_sorted_job_ids(db_session, TestResult.travis_job_id, limit)


def get_travis_builds(db_session, limit=None):
    """ Returns a decreasing sorted list of Travis job ids that collected Endpoint data. """
    return get_sorted_job_ids(db_session, TestEndpoint.travis_job_id, limit)


def get_suite_measurements(db_session, suite):
    """ Return all measurements for some Travis build. Used for creating a box plot. """
    result = [result[0] for result in
              db_session.query(TestResult.execution_time).filter(TestResult.travis_job_id == suite).all()]
    return result if len(result) > 0 else [0]


def get_endpoint_measurements(db_session, suite):
    """ Return all measurements for some Travis build. Used for creating a box plot. """
    result = [result[0] for result in
              db_session.query(TestEndpoint.execution_time).filter(TestEndpoint.travis_job_id == suite).all()]
    return result if len(result) > 0 else [0]


def get_endpoint_measurements_job(db_session, name, job_id):
    """ Return all measurements for some test of some Travis build. Used for creating a box plot. """
    endpoint_id = db_session.query(Endpoint.id).filter(Endpoint.name == name).first()[0]
    result = db_session.query(TestEndpoint).filter(
        TestEndpoint.endpoint_id == endpoint_id).filter(TestEndpoint.travis_job_id == job_id).options(
        joinedload(TestEndpoint.endpoint)).all()
    return [r.execution_time for r in result] if len(result) > 0 else [0]


def get_last_tested_times(db_session):
    """ Returns the last tested time of each of the endpoints. """
    return db_session.query(TestEndpoint.endpoint.name, func.max(TestEndpoint.time_added)).group_by(
        TestEndpoint.endpoint.name).options(joinedload(TestEndpoint.endpoint)).all()
