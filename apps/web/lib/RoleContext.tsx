"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';

export type UserRole = 'traveller' | 'highway' | 'district' | 'research';

interface RoleContextType {
  role: UserRole;
  setRole: (role: UserRole) => void;
  isModalOpen: boolean;
  setIsModalOpen: (open: boolean) => void;
  openRoleModal: () => void;
}

const RoleContext = createContext<RoleContextType | undefined>(undefined);

export function RoleProvider({ children }: { children: ReactNode }) {
  const [role, setRoleState] = useState<UserRole>('traveller');
  const [isModalOpen, setIsModalOpen] = useState<boolean>(false);
  const [hasInitialized, setHasInitialized] = useState<boolean>(false);

  useEffect(() => {
    try {
      const savedRole = localStorage.getItem('geoslide_user_role') as UserRole;
      if (savedRole && ['traveller', 'highway', 'district', 'research'].includes(savedRole)) {
        setRoleState(savedRole);
      } else {
        // First visit: open modal
        setIsModalOpen(true);
      }
    } catch (e) {
      console.warn('localStorage unavailable for GeoSlide role persistence:', e);
    } finally {
      setHasInitialized(true);
    }
  }, []);

  const setRole = (newRole: UserRole) => {
    setRoleState(newRole);
    try {
      localStorage.setItem('geoslide_user_role', newRole);
    } catch (e) {
      console.warn('Failed to persist role in localStorage:', e);
    }
  };

  const openRoleModal = () => {
    setIsModalOpen(true);
  };

  return (
    <RoleContext.Provider value={{ role, setRole, isModalOpen, setIsModalOpen, openRoleModal }}>
      {children}
    </RoleContext.Provider>
  );
}

export function useUserRole() {
  const context = useContext(RoleContext);
  if (!context) {
    throw new Error('useUserRole must be used within a RoleProvider');
  }
  return context;
}
