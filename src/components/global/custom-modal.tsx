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
  // Provider open state, or defaultOpen if you ever want it forced on (sidebar uses setOpen instead).
  const open = isOpen || !!defaultOpen;

  return (
    <Dialog open={open} onOpenChange={(next) => { if (!next) setClose(); }}>
      {/* Scroll on small screens; sit above the mobile burger (z-100). */}
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
