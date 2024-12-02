'use client';

import React, { useState } from 'react';
import { useFormik } from 'formik';
import * as Yup from 'yup';

const API_URL = "https://contact.cloudbend.dev";

const Spinner = () => (
    <div className="animate-spin rounded-full h-5 w-5 border-t-2 border-b-2 border-white"></div>
);

const ContactForm = () => {
    const [submitted, setSubmitted] = useState(false);

    const formik = useFormik({
        initialValues: {
            email: '',
            message: '',
        },
        validationSchema: Yup.object({
            email: Yup.string().email('Invalid email address').required('Required'),
            message: Yup.string().required('Required'),
        }),
        onSubmit: (values) => {
            fetch(API_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(values),
            })
                .then((response) => response.json())
                .then((_) => {
                    setSubmitted(true);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        },
    });

    if (submitted) {
        return (
            <div className="text-center text-gray-800">
                We've received your message! Expect us to follow up soon.
            </div>
        );
    }

    return (
        <form onSubmit={formik.handleSubmit}>
            <div className="mb-4">
                <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                    Email
                </label>
                <input
                    type="email"
                    name="email"
                    id="email"
                    value={formik.values.email}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
                />
                {formik.touched.email && formik.errors.email ? (
                    <div className="text-red-500 text-sm">{formik.errors.email}</div>
                ) : null}
            </div>
            <div className="mb-4">
                <label htmlFor="message" className="block text-sm font-medium text-gray-700">
                    Message
                </label>
                <textarea
                    name="message"
                    id="message"
                    rows={4}
                    value={formik.values.message}
                    onChange={formik.handleChange}
                    onBlur={formik.handleBlur}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 text-gray-900"
                />
                {formik.touched.message && formik.errors.message ? (
                    <div className="text-red-500 text-sm">{formik.errors.message}</div>
                ) : null}
            </div>
            <div className="mb-4">
                <button
                    type="submit"
                    className="w-full flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                >
                    {!formik.isValidating && formik.isSubmitting ? (
                        <Spinner />
                    ) : (
                        'Submit'
                    )}
                </button>
            </div>
        </form>
    );
};

export default ContactForm;