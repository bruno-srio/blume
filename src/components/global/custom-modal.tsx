import { useModal } from "@/providers/modal-provider";
import React from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";


type Props = {
  title: string;
  subheading: string;
  children: React.ReactNode;
  defaultOpen?: boolean;
};

const CustomModal = ({ title, subheading, children, defaultOpen }: Props) => {
  const { isOpen, setClose } = useModal();
  const open = isOpen || !!defaultOpen;

  return (
    <Dialog open={open} onOpenChange={(next) => { if (!next) setClose(); }}>
      {/* max-h + overflow on all breakpoints so tall forms scroll on mobile; z above burger (z-100) */}
      <DialogContent className="z-[110] max-h-[90vh] overflow-y-auto md:max-h-[700px] bg-card">
        <DialogHeader className="pt-8 text-left">
          <DialogTitle className="text-2xl font-bold">{title}</DialogTitle>
          <DialogDescription>{subheading}</DialogDescription>
          {children}
        </DialogHeader>
      </DialogContent>
    </Dialog>
  );
};

export default CustomModal;
