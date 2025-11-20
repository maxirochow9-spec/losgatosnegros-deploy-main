param(
    [string]$branch = "feature/auth",
    [string]$message = "feat: snapshot before adding auth — DB/settings/import command/fixtures"
)

Write-Host "Checking git status..."
git status

# Create branch if it doesn't exist
$exists = git branch --list $branch
if (-not $exists) {
    Write-Host "Creating branch $branch"
    git checkout -b $branch
} else {
    Write-Host "Switching to existing branch $branch"
    git checkout $branch
}

Write-Host "Adding all changes..."
git add -A

Write-Host "Committing with message: $message"
# If there's nothing to commit, this will exit non-zero; catch and continue
try {
    git commit -m "$message"
} catch {
    Write-Host "No changes to commit or commit failed: $_"
}

Write-Host "Pushing to origin/$branch"
git push -u origin $branch

Write-Host "Done. Review output above for any errors."
