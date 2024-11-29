import React, { useState } from 'react';
import apiService from '../services/apiService';

function QuestComponent() {
    const [userId, setUserId] = useState('');
    const [paymentId, setPaymentId] = useState('');
    const [response, setResponse] = useState(null);

    const handleQuestCompletion = async () => {
        const result = await apiService.completeQuest(userId, paymentId);
        setResponse(result);
    };

    return (
        <div>
            <h2>Complete a Quest</h2>
            <input
                type="text"
                placeholder="User ID"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
            />
            <input
                type="text"
                placeholder="Payment ID"
                value={paymentId}
                onChange={(e) => setPaymentId(e.target.value)}
            />
            <button onClick={handleQuestCompletion}>Complete Quest</button>
            {response && <p>{response.message}</p>}
        </div>
    );
}

export default QuestComponent;

