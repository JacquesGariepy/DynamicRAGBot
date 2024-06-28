import React from 'react';
import { Box, AppBar, Toolbar, Typography, Drawer, List, ListItem, ListItemIcon, ListItemText } from '@mui/material';
import { Link } from 'react-router-dom';
import { Dashboard as DashboardIcon, Build as BuildIcon, Description as DescriptionIcon, Storage as StorageIcon, Settings as SettingsIcon } from '@mui/icons-material';
import { useAuth } from '../context/AuthContext';

const drawerWidth = 240;

function Layout({ children }) {
    const { isAuthenticated, logout } = useAuth();

    const menuItems = [
        { text: 'Dashboard', icon: <DashboardIcon />, path: '/' },
        { text: 'Bots', icon: <BuildIcon />, path: '/bots' },
        { text: 'Documents', icon: <DescriptionIcon />, path: '/documents' },
        { text: 'RAG Interface', icon: <StorageIcon />, path: '/rag' },
        { text: 'Settings', icon: <SettingsIcon />, path: '/settings' },
    ];

    return (
        <Box sx={{ display: 'flex' }}>
            <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
                <Toolbar>
                    <Typography variant="h6" noWrap component="div">
                        RAG Bot Manager
                    </Typography>
                </Toolbar>
            </AppBar>
            {isAuthenticated && (
                <Drawer
                    variant="permanent"
                    sx={{
                        width: drawerWidth,
                        flexShrink: 0,
                        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
                    }}
                >
                    <Toolbar />
                    <Box sx={{ overflow: 'auto' }}>
                        <List>
                            {menuItems.map((item) => (
                                <ListItem button key={item.text} component={Link} to={item.path}>
                                    <ListItemIcon>{item.icon}</ListItemIcon>
                                    <ListItemText primary={item.text} />
                                </ListItem>
                            ))}
                        </List>
                    </Box>
                </Drawer>
            )}
            <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
                <Toolbar />
                {children}
            </Box>
        </Box>
    );
}

export default Layout;