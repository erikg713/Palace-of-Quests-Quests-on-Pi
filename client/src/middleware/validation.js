// validation.js

/**
 * Validation Middleware
 * Intercepts Redux actions to validate their payloads before they reach the reducers.
 */

import { setError, clearError } from '../slices/errorSlice';
import Joi from 'joi';

/**
 * Define validation schemas for different action types.
 * Extend this object with schemas for other actions as needed.
 */
const validationSchemas = {
    'user/login': Joi.object({
        email: Joi.string().email().required(),
        password: Joi.string().min(6).required(),
    }),
    'user/register': Joi.object({
        name: Joi.string().min(3).required(),
        email: Joi.string().email().required(),
        password: Joi.string().min(6).required(),
    }),
    'product/createProduct': Joi.object({
        name: Joi.string().min(3).required(),
        price: Joi.number().positive().required(),
        description: Joi.string().min(10).required(),
        category: Joi.string().required(),
        stock: Joi.number().integer().min(0).required(),
        imageUrl: Joi.string().uri().optional(),
    }),
    // Add more schemas for other actions here
};

/**
 * Validation Middleware Function
 * @param {Object} store - The Redux store.
 */
const validationMiddleware = (store) => (next) => (action) => {
    const { type, payload } = action;

    // Check if there's a validation schema for the current action type
    const schema = validationSchemas[type];
    if (schema) {
        const { error } = schema.validate(payload, { abortEarly: false });

        if (error) {
            // Aggregate all validation error messages
            const errorMessages = error.details.map((detail) => detail.message).join('; ');

            // Dispatch the error to the error slice
            store.dispatch(setError(`Validation Error (${type}): ${errorMessages}`));

            // Optionally, prevent the action from reaching reducers
            return;
        } else {
            // Clear any existing errors if validation passes
            store.dispatch(clearError());
        }
    }

    // Pass the action to the next middleware or reducer
    return next(action);
};

export default validationMiddleware;
