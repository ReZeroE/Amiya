#include <windows.h>
#include <stdio.h>


// C:\Program Files (x86)\Windows Kits\10\Include\10.0.19041.0\um\ShellScalingApi.h

BOOL isFullscreen(HWND hwnd) {
    // Get the screen size
    RECT screen;
    screen.left = GetSystemMetrics(SM_XVIRTUALSCREEN);
    screen.top = GetSystemMetrics(SM_YVIRTUALSCREEN);
    screen.right = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    screen.bottom = GetSystemMetrics(SM_CYVIRTUALSCREEN);

    // Get the window rect
    RECT winRect;
    GetWindowRect(hwnd, &winRect);

    // Compare window size to screen size
    return (winRect.left == screen.left && 
            winRect.top == screen.top &&
            winRect.right == screen.right && 
            winRect.bottom == screen.bottom);
}

BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam) {
    DWORD lpdwProcessId;
    GetWindowThreadProcessId(hwnd, &lpdwProcessId);
    if (lpdwProcessId == lParam) {
        // Once we find the first top-level window for the PID, stop enumerating
        char title[256];
        GetWindowText(hwnd, title, sizeof(title));
        if (IsWindowVisible(hwnd) && strlen(title) > 0) {
            // Check if this is a main window
            RECT rect;
            GetWindowRect(hwnd, &rect);
            int width = rect.right - rect.left;
            int height = rect.bottom - rect.top;
            BOOL fullscreen = isFullscreen(hwnd);
            printf("%d %d %d\n", width, height, fullscreen);
            return FALSE; // Stop enumerating windows
        }
    }
    return TRUE; // Continue enumerating
}


int main(int argc, char *argv[]) {

    if (argc != 2) {
        fprintf(stderr, "Usage: %s <PID>\n", argv[0]);
        return 1;
    }

    DWORD pid = (DWORD)atoi(argv[1]);
    EnumWindows(EnumWindowsProc, (LPARAM)pid);
    return 0;
}