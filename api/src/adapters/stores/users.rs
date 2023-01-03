use crate::domain::interfaces::stores;
use ::inject::*;
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
}
