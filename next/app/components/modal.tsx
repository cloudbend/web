"use client";

import React, { ReactNode, useState } from 'react';

type ModalProps = {
    onClose: () => void;
    children: ReactNode | ReactNode[];
};

const Modal = ({ onClose, children }: ModalProps) => (
    <div className="fixed inset-0 z-50 flex items-center justify-center backdrop-blur-sm" onClick={onClose}>
        <div className="bg-white rounded-lg overflow-hidden shadow-xl p-8">
            <button onClick={onClose} className="close-button">Close</button>
            {children}
        </div>
    </div>
);

type ModalButtonProps = {
    className?: string;
    label: string;
    children: ReactNode | ReactNode[];
};

const ModalButton = ({ className, label, children }: ModalButtonProps) => {
    const [isOpen, setIsOpen] = useState(false);
    const open = () => setIsOpen(true);
    const close = () => setIsOpen(false);

    return (
        <>
            <button className={className} onClick={open}>{label}</button>
            {isOpen && <Modal onClose={close}>{children}</Modal>}
        </>
    );
};

export { ModalButton };
export default Modal;