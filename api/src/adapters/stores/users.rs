use crate::adapters::stores::models::users::Users as UserModel;
use crate::domain::interfaces::stores;
use ::inject::*;
use diesel::prelude::*;
use diesel::PgConnection;
pub struct Users<'a> {
    con: &'a mut PgConnection,
}

impl<'a> Users<'a> {
    #[inject]
    fn new(con: &mut PgConnection) -> Self {
        Self { con }
    }
}

impl<'a> stores::Users for Users<'a> {
    fn create(&self, u: crate::domain::entities::User) {}
    fn get(&self, name: String) -> crate::domain::entities::User {
        let res =
    }
}
