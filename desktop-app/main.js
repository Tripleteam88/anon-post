const { app, BrowserWindow, Menu, screen } = require('electron');

// Create window Electron boilerplate
var win = null;
function createWindow(url='https://anonpost.jasonli0616.repl.co') {
    const mainScreen = screen.getPrimaryDisplay();
    win = new BrowserWindow({
        width: mainScreen.size.width,
        height: mainScreen.size.height,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    win.loadURL(url);
}

app.whenReady().then(() => {
    createWindow();
  
    app.on('activate', function() {
        if (BrowserWindow.getAllWindows().length === 0) { createWindow(); }
    });
});

app.on('window-all-closed', function() {
    if (process.platform !== 'darwin') { app.quit(); }
});

const isMac = (process.platform === 'darwin');

// Menu bar
Menu.setApplicationMenu(
    Menu.buildFromTemplate([
        // Menubar show App menu if on Mac
        ...(isMac ? [
            { role: 'appMenu' },
        ] : []),
        { role: 'fileMenu' },
        { role: 'editMenu' },
        {
            label: 'User',
            submenu: [
                {
                    label: 'Login',
                    click: () => {
                        win.destroy()
                        createWindow('https://anonpost.jasonli0616.repl.co/login');
                    },
                },
                {
                    label: 'Sign up',
                    click: () => {
                        win.destroy()
                        createWindow('https://anonpost.jasonli0616.repl.co/signup');
                    },
                },
                { type: 'separator' },
                {
                    label: 'Create post',
                    click: () => {
                        win.destroy()
                        createWindow('https://anonpost.jasonli0616.repl.co/create');
                    },
                },
                { type: 'separator' },
                {
                    label: 'Signout',
                    click: () => {
                        win.destroy()
                        createWindow('https://anonpost.jasonli0616.repl.co/logout');
                    },
                },
            ],
        },
        { role: 'windowMenu' },

    ])
)