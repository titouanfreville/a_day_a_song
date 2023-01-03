use crate::domain::entities;

pub trait Users {
    fn create(&self, u: entities::User);
    // fn update(u: entities::User);
    fn get(&self, name: String) -> entities::User;
    // fn list() -> vector<entities::User>;
}
