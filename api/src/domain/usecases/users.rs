use crate::domain::entities;
use crate::domain::interfaces::stores;
use ::inject::*;
use uuid::Uuid;

pub struct Users<'a> {
    store: &'a dyn stores::Users,
}

impl<'a> Users<'a> {
    #[inject]
    fn new(store: &dyn stores::Users) -> Self {
        Self { store }
    }

    fn create(&self, username: String) -> entities::User {
        let usr = entities::User {
            id: Uuid::new_v4(),
            name: username,
        };

        self.store.create(usr);

        return usr;
    }

    fn get(&self, username: String) -> entities::User {
        return self.store.get(username);
    }
}
