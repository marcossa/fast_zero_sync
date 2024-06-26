from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='marcos',
        email='marcos@fast_zero.net',
        password='senha123',
    )
    session.add(new_user)
    session.commit

    user = session.scalar(select(User).where(User.username == 'marcos'))

    assert user.username == 'marcos'
