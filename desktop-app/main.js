const { app, BrowserWindow, Menu, screen } = require('electron');
require('electron-reload')(__dirname);

function createWindow() {
    const mainScreen = screen.getPrimaryDisplay()
    const win = new BrowserWindow({
        width: mainScreen.size.width,
        height: mainScreen.size.height,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
        },
    });

    win.loadURL('https://anonpost.jasonli0616.repl.co');

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