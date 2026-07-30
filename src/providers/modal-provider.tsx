'use client'

import { Agency, Contact, User } from '@/generated/prisma'
import { createContext, useContext, useEffect, useState } from 'react'

interface ModalProviderProps {
    children: React.ReactNode
}

export type ModalData = {
    user?: User
    agency?: Agency
}

type ModalContextType = {
    data: ModalData;
    isOpen: boolean;
    setOpen: (modal: React.ReactNode, fetchData?: () => Promise<any>) => void;
    setClose: () => void;
  };

  export const ModalContext = createContext<ModalContextType>({
    data: {},
    isOpen: false,
    setOpen: (modal: React.ReactNode, fetchData?: () => Promise<any>) => {},
    setClose: () => {},
  });
  
  const ModalProvider: React.FC<ModalProviderProps> = ({ children }) => {
    const [isOpen, setIsOpen] = useState(false);
    const [data, setData] = useState<ModalData>({});
    const [showingModal, setShowingModal] = useState<React.ReactNode>(null);
    const [isMounted, setIsMounted] = useState(false);
  
    useEffect(() => {
      setIsMounted(true);
    }, []);
  
    const setOpen = async (
      modal: React.ReactNode,
      fetchData?: () => Promise<any>
    ) => {
      if (modal) {
        if (fetchData) {
          // Merge async payload into modal context before opening so the modal can read it via useModal()
          // Fallback on the await result, a merged object is always truthy, so || {} outside would never run
          setData({ ...data, ...((await fetchData()) || {}) })
        }
        setShowingModal(modal);
        setIsOpen(true);
      }
    };
  
    const setClose = () => {
      setIsOpen(false);
      setData({});
    };
  
    if (!isMounted) return null;
  
    return (
      <ModalContext.Provider value={{ data, setOpen, setClose, isOpen }}>
        {children}
        {showingModal}
      </ModalContext.Provider>
    );
  };
  
  export const useModal = () => {
    const context = useContext(ModalContext);
    if (!context) {
      throw new Error("useModal must be used within a Modal Provider");
    }
    return context;
  };
  
  export default ModalProvider;