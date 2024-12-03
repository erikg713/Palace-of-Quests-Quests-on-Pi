// productRoutes.js

import React, { lazy } from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth'; // Custom hook for authentication

// Lazy-loaded Components for Code Splitting
const ProductList = lazy(() => import('../pages/Products/ProductList'));
const ProductDetails = lazy(() => import('../pages/Products/ProductDetails'));
const CreateProduct = lazy(() => import('../pages/Products/CreateProduct'));
const EditProduct = lazy(() => import('../pages/Products/EditProduct'));
const ProductSuccess = lazy(() => import('../pages/Products/ProductSuccess'));
const ProductFailure = lazy(() => import('../pages/Products/ProductFailure'));

/**
 * ProtectedRoute Component
 * Ensures that only authenticated users can access certain routes.
 */
const ProtectedRoute = ({ children }) => {
    const { isAuthenticated } = useAuth();

    if (!isAuthenticated) {
        // Redirect to login page if not authenticated
        return <Navigate to="/login" replace />;
    }

    return children;
};

/**
 * Product Routes Configuration
 * Defines all the routes related to products in the application.
 */
const productRoutes = [
    {
        path: '/products',
        element: (
            <ProtectedRoute>
                <ProductList />
            </ProtectedRoute>
        ),
        name: 'Product List',
        exact: true,
    },
    {
        path: '/products/:productId',
        element: (
            <ProtectedRoute>
                <ProductDetails />
            </ProtectedRoute>
        ),
        name: 'Product Details',
        exact: true,
    },
    {
        path: '/products/create',
        element: (
            <ProtectedRoute>
                <CreateProduct />
            </ProtectedRoute>
        ),
        name: 'Create Product',
        exact: true,
    },
    {
        path: '/products/edit/:productId',
        element: (
            <ProtectedRoute>
                <EditProduct />
            </ProtectedRoute>
        ),
        name: 'Edit Product',
        exact: true,
    },
    {
        path: '/product-success',
        element: <ProductSuccess />,
        name: 'Product Success',
        exact: true,
    },
    {
        path: '/product-failure',
        element: <ProductFailure />,
        name: 'Product Failure',
        exact: true,
    },
];

export default productRoutes;
