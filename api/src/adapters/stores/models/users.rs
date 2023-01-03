use diesel::prelude::Queryable;
use uuid::Uuid;

#[derive(Queryable)]
pub struct Users {
    pub id: Uuid,
    pub name: String,
}
