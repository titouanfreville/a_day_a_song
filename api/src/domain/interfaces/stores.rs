use crates::domain::entities;

pub trait User {
    fn create(u: entities::User);
    fn update(u: entities::User);
    fn get() -> entities::User;
    fn list() -> vector<entities::User>;
}
