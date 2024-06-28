import React, { useState, useEffect } from 'react';
import { getBots, createBot, startBot, stopBot, deleteBot, performBotAction } from '../services/botService';

function BotManagement() {
    const [bots, setBots] = useState([]);
    const [newBotName, setNewBotName] = useState('');
    const [newBotConfig, setNewBotConfig] = useState('');
    const [actionType, setActionType] = useState('');
    const [actionParams, setActionParams] = useState('');
    const [selectedBotId, setSelectedBotId] = useState('');

    useEffect(() => {
        fetchBots();
    }, []);

    const fetchBots = async () => {
        try {
            const fetchedBots = await getBots();
            setBots(fetchedBots);
        } catch (error) {
            console.error('Error fetching bots:', error);
        }
    };

    const handleCreateBot = async () => {
        try {
            const config = JSON.parse(newBotConfig);
            await createBot(newBotName, config);
            setNewBotName('');
            setNewBotConfig('');
            fetchBots();
        } catch (error) {
            console.error('Error creating bot:', error);
        }
    };

    const handleStartBot = async (botId) => {
        try {
            await startBot(botId);
            fetchBots();
        } catch (error) {
            console.error('Error starting bot:', error);
        }
    };

    const handleStopBot = async (botId) => {
        try {
            await stopBot(botId);
            fetchBots();
        } catch (error) {
            console.error('Error stopping bot      }
    };

    const handleDeleteBot = async (botId) => {
        try {
            await deleteBot(botId);
            fetchBots();
        } catch (error) {
            console.error('Error deleting bot:', error);
        }
    };

    const handlePerformAction = async () => {
        if (!selectedBotId) {
            console.error('No bot selected for action');
            return;
        }
        try {
            const params = JSON.parse(actionParams);
            const result = await performBotAction(selectedBotId, actionType, params);
            console.log('Action result:', result);
            // Vous pouvez ajouter ici une logique pour afficher le résultat à l'utilisateur
        } catch (error) {
            console.error('Error performing bot action:', error);
        }
    };

    return (
        <div>
            <h1>Bot Management</h1>
            <div>
                <input
                    type="text"
                    value={newBotName}
                    onChange={(e) => setNewBotName(e.target.value)}
                    placeholder="Bot Name"
                />
                <textarea
                    value={newBotConfig}
                    onChange={(e) => setNewBotConfig(e.target.value)}
                    placeholder="Bot Configuration (JSON)"
                />
                <button onClick={handleCreateBot}>Create Bot</button>
            </div>
            <ul>
                {bots.map(bot => (
                    <li key={bot.id}>
                        {bot.name} - Status: {bot.status}
                        <button onClick={() => handleStartBot(bot.id)}>Start</button>
                        <button onClick={() => handleStopBot(bot.id)}>Stop</button>
                        <button onClick={() => handleDeleteBot(bot.id)}>Delete</button>
                        <button onClick={() => setSelectedBotId(bot.id)}>Select</button>
                    </li>
                ))}
            </ul>
            <div>
                <h2>Perform Bot Action</h2>
                <select value={actionType} onChange={(e) => setActionType(e.target.value)}>
                    <option value="">Select Action Type</option>
                    <option value="scrape">Scrape</option>
                    <option value="query">Query</option>
                </select>
                <textarea
                    value={actionParams}
                    onChange={(e) => setActionParams(e.target.value)}
                    placeholder="Action Parameters (JSON)"
                />
                <button onClick={handlePerformAction}>Perform Action</button>
            </div>
        </div>
    );
}

export default BotManagement;
