#include <windows.h>
#include <stdio.h>

// Compile:
//     gcc .\scripts\focus_pid.c -o focus_pid -luser32

BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam) {
    DWORD dwPID;
    GetWindowThreadProcessId(hwnd, &dwPID);

    if (dwPID == (DWORD)lParam) {
        BOOL ret = SetForegroundWindow(hwnd);   // Try to bring window to foreground
        return FALSE;                           // Stop enumeration
    }
    return TRUE;                                // Continue enumeration
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <PID>\n", argv[0]);
        return 1;
    }
    // printf("PID: %s\n", argv[1]);

    DWORD pid = (DWORD)atoi(argv[1]);
    EnumWindows(EnumWindowsProc, (LPARAM)pid);
    return 0;
}