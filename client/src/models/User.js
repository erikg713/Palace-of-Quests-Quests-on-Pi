// User.js

/**
 * User Model
 * Represents a user entity within the Palace of Quests application.
 */

class User {
    /**
     * Creates an instance of User.
     * @param {Object} params - User parameters.
     * @param {string} params.id - Unique identifier for the user.
     * @param {string} params.name - Full name of the user.
     * @param {string} params.email - Email address of the user.
     * @param {string} params.role - Role of the user ('user', 'admin').
     * @param {Date} params.createdAt - Date and time when the user was created.
     * @param {Date} params.updatedAt - Date and time when the user was last updated.
     * @param {string} [params.avatarUrl] - Optional URL to the user's avatar image.
     * @param {string} [params.bio] - Optional biography or description of the user.
     */
    constructor({ id, name, email, role, createdAt, updatedAt, avatarUrl = '', bio = '' }) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.role = role;
        this.createdAt = createdAt instanceof Date ? createdAt : new Date(createdAt);
        this.updatedAt = updatedAt instanceof Date ? updatedAt : new Date(updatedAt);
        this.avatarUrl = avatarUrl;
        this.bio = bio;
    }

    /**
     * Updates the user's profile information.
     * @param {Object} updates - An object containing the fields to update.
     * @param {string} [updates.name] - New name of the user.
     * @param {string} [updates.email] - New email address of the user.
     * @param {string} [updates.avatarUrl] - New avatar URL of the user.
     * @param {string} [updates.bio] - New biography of the user.
     */
    updateProfile({ name, email, avatarUrl, bio }) {
        if (name !== undefined) this.name = name;
        if (email !== undefined) this.email = email;
        if (avatarUrl !== undefined) this.avatarUrl = avatarUrl;
        if (bio !== undefined) this.bio = bio;
        this.updatedAt = new Date();
    }

    /**
     * Updates the user's role.
     * @param {string} newRole - The new role ('user', 'admin').
     */
    updateRole(newRole) {
        const validRoles = ['user', 'admin'];
        if (!validRoles.includes(newRole)) {
            throw new Error(`Invalid role: ${newRole}. Valid roles are ${validRoles.join(', ')}`);
        }
        this.role = newRole;
        this.updatedAt = new Date();
    }

    /**
     * Formats the creation date to a readable string.
     * @returns {string} - Formatted creation date string.
     */
    getFormattedCreationDate() {
        return this.createdAt.toLocaleString();
    }

    /**
     * Formats the last updated date to a readable string.
     * @returns {string} - Formatted updated date string.
     */
    getFormattedUpdatedDate() {
        return this.updatedAt.toLocaleString();
    }

    /**
     * Returns a summary of the user.
     * @returns {string} - Summary string.
     */
    getSummary() {
        return `${this.name} (${this.email}) - Role: ${this.role}.`;
    }

    /**
     * Checks if the user has admin privileges.
     * @returns {boolean} - True if user is an admin, else false.
     */
    isAdmin() {
        return this.role === 'admin';
    }
}

export default User;
