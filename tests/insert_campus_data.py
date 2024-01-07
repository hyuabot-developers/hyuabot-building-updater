from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from models import Campus


async def insert_campus_data(db_session: Session):
    insert_statement = insert(Campus).values(
        [
            dict(campus_id=1, campus_name="서울"),
            dict(campus_id=2, campus_name="ERICA"),
        ]
    )
    insert_statement = insert_statement.on_conflict_do_update(
        index_elements=["campus_id"],
        set_=dict(campus_name=insert_statement.excluded.campus_name),
    )
    db_session.execute(insert_statement)
    db_session.commit()
