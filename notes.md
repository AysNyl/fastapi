what does --set-upstream flag do? https://stackoverflow.com/questions/18031946/when-doing-a-git-push-what-does-set-upstream-do

- First answer    
    git branch --set-upstream-to <remote-branch>

    sets the default remote branch for the current local branch.

    Any future git pull command (with the current local branch checked-out),
    will attempt to bring in commits from the <remote-branch> into the current local branch.

    git push -u origin <local-branch>
    This automatically creates an upstream counterpart branch for any future push/pull attempts from teh current <local-branch>. The upstream remote branch derived from the branch name - <local-branch> is also configured as the default for all subsequent actions like push/pull etc.

    For more details, check out this detailed explanation about upstream branches and tracking.


    For example, executing the above command for <local-branch> = test,
    will result in creating a <remote branch> = remotes/origin/test.

    Note: One way to avoid having to explicitly type --set-upstream / --set-upstream-to is to use its shorthand flag -u.


- Second answer
    When you push to a remote and you use the --set-upstream flag git sets the branch you are pushing to as the remote tracking branch of the branch you are pushing.

    Adding a remote tracking branch means that git then knows what you want to do when you git fetch, git pull or git push in future. It assumes that you want to keep the local branch and the remote branch it is tracking in sync and does the appropriate thing to achieve this.

    You could achieve the same thing with git branch --set-upstream-to or git checkout --track. See the git help pages on tracking branches for more information.
