import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './styles/theme';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import BotManagement from './pages/BotManagement';
import DocumentManagement from './pages/DocumentManagement';
import RAGInterface from './pages/RAGInterface';
import Settings from './pages/Settings';
import Login from './pages/Login';
import Register from './pages/Register';
import PrivateRoute from './components/PrivateRoute';

function App() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <Router>
                <Layout>
                    <Switch>
                        <Route path="/login" component={Login} />
                        <Route path="/register" component={Register} />
                        <PrivateRoute exact path="/" component={Dashboard} />
                        <PrivateRoute path="/bots" component={BotManagement} />
                        <PrivateRoute path="/documents" component={DocumentManagement} />
                        <PrivateRoute path="/rag" component={RAGInterface} />
                        <PrivateRoute path="/settings" component={Settings} />
                    </Switch>
                </Layout>
            </Router>
        </ThemeProvider>
    );
}

export default App;