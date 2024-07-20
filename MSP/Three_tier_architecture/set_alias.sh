# Functions
function restart-pwsh {
    clear
    Invoke-Command { & "pwsh.exe" } -NoNewScope
}

# Alias
Set-Alias psd pushd
Set-Alias ppd popd
Set-Alias clr clear
Set-Alias restart restart-pwsh
Set-Alias terraform "D:\terraform.exe"
Set-Alias tf "D:\terraform.exe"