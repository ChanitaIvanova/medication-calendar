import React, { createContext, useContext, useState, ReactNode } from 'react';
import User from '../types/User'

interface UserContextType {
    user: User | null;
    setUser: (user: User) => void;
    clearUser: () => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const useUser = () => {
    const context = useContext(UserContext);
    if (!context) {
        throw new Error('useUser must be used within a UserProvider');
    }
    return context;
};

export const UserProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [user, setUserState] = useState<User | null>(null);
  
    const setUser = (user: User) => {
      setUserState(user);
    };
  
    const clearUser = () => {
      setUserState(null);
    };
  
    return (
      <UserContext.Provider value={{ user, setUser, clearUser }}>
        {children}
      </UserContext.Provider>
    );
  };