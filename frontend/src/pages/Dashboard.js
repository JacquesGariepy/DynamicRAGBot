import React, { useState, useEffect } from 'react';
import { Grid, Paper, Typography } from '@mui/material';
import { getBots } from '../services/botService';
import { getRAGStats } from '../services/ragService';

function Dashboard() {
    const [bots, setBots] = useState([]);
    const [ragStats, setRagStats] = useState({});

    useEffect(() => {
        fetchBots();
        fetchRAGStats();
    }, []);

    const fetchBots = async () => {
        try {
            const fetchedBots = await getBots();
            setBots(fetchedBots);
        } catch (error) {
            console.error('Error fetching bots:', error);
        }
    };

    const fetchRAGStats = async () => {
        try {
            const stats = await getRAGStats();
            setRagStats(stats);
        } catch (error) {
            console.error('Error fetching RAG stats:', error);
        }
    };

    return (
        <Grid container spacing={3}>
            <Grid item xs={12}>
                <Typography variant="h4" gutterBottom>
                    Dashboard
                </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>
                        Active Bots
                    </Typography>
                    {bots.map(bot => (
                        <Typography key={bot.id}>
                            {bot.name} - Status: {bot.status}
                        </Typography>
                    ))}
                </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
                <Paper sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>
                        RAG System Statistics
                    </Typography>
                    <Typography>Total Documents: {ragStats.totalDocuments}</Typography>
                    <Typography>Queries Today: {ragStats.queriesToday}</Typography>
                </Paper>
            </Grid>
        </Grid>
    );
}

export default Dashboard;