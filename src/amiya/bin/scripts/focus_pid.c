// #include <windows.h>
// #include <stdio.h>

// // Compile:
// //     gcc .\scripts\focus_pid.c -o focus_pid -luser32

// BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam) {
//     DWORD dwPID;
//     GetWindowThreadProcessId(hwnd, &dwPID);

//     if (dwPID == (DWORD)lParam) {
//         BOOL ret = SetForegroundWindow(hwnd);   // Try to bring window to foreground
//         return FALSE;                           // Stop enumeration
//     }
//     return TRUE;                                // Continue enumeration
// }

// int main(int argc, char *argv[]) {
//     if (argc != 2) {
//         printf("Usage: %s <PID>\n", argv[0]);
//         return 1;
//     }
//     // printf("PID: %s\n", argv[1]);

//     DWORD pid = (DWORD)atoi(argv[1]);
//     EnumWindows(EnumWindowsProc, (LPARAM)pid);
//     return 0;
// }

#include <windows.h>
#include <stdio.h>

BOOL CALLBACK EnumWindowsProc(HWND hwnd, LPARAM lParam) {
    DWORD dwPID;
    GetWindowThreadProcessId(hwnd, &dwPID);

    if (dwPID == (DWORD)lParam) {
        // Check if the window is visible
        if (!IsWindowVisible(hwnd)) {
            ShowWindow(hwnd, SW_RESTORE);  // Attempt to restore the window if it's minimized or hidden
        }

        // Try to bring window to foreground
        if (!SetForegroundWindow(hwnd)) {
            printf("Failed to set window to foreground.\n");
        }
        return FALSE;  // Stop enumeration as we have found and processed the window
    }
    return TRUE;  // Continue enumeration if not the desired window
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <PID>\n", argv[0]);
        return 1;
    }

    DWORD pid = (DWORD)atoi(argv[1]);
    EnumWindows(EnumWindowsProc, (LPARAM)pid);
    return 0;
}
