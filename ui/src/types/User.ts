export type UserRole = 'admin' | 'user';

export default interface User {
    user_id: string;
    username: string;
    email: string;
    role: UserRole;
}
