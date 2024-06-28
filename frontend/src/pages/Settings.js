import React, { useState, useEffect } from 'react';
import { getSettings, updateSettings } from '../services/settingsService';

function Settings() {
    const [settings, setSettings] = useState({});

    useEffect(() => {
        fetchSettings();
    }, []);

    const fetchSettings = async () => {
        try {
            const fetchedSettings = await getSettings();
            setSettings(fetchedSettings);
        } catch (error) {
            console.error('Error fetching settings:', error);
        }
    };

    const handleChange = (e) => {
        const { name, value } = e.target;
        setSettings(prevSettings => ({ ...prevSettings, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await updateSettings(settings);
            alert('Settings updated successfully');
        } catch (error) {
            console.error('Error updating settings:', error);
            alert('Failed to update settings');
        }
    };

    return (
        <div>
            <h1>Settings</h1>
            <form onSubmit={handleSubmit}>
                <div>
                    <label htmlFor="apiKey">API Key:</label>
                    <input
                        type="text"
                        id="apiKey"
                        name="apiKey"
                        value={settings.apiKey || ''}
                        onChange={handleChange}
                    />
                </div>
                <div>
                    <label htmlFor="maxBots">Max Bots:</label>
                    <input
                        type="number"
                        id="maxBots"
                        name="maxBots"
                        value={settings.maxBots || ''}
                        onChange={handleChange}
                    />
                </div>
                <button type="submit">Save Settings</button>
            </form>
        </div>
    );
}

export default Settings;