; Specify how the gerritevent.Dispatcher connects to your gerrit host.

[gerrit]
user: alice
host: gerritserver
port: 29418
passphrase: tester
ssh_private_key: /home/YOURLOGIN/.ssh/id_rsa_alice

; Specify how the gerritevent.RedmineHandler can push updates to your Redmine
; instance.

[redmine]

; API-Key
;
; The API-Key can be found in Redmine under "My Account" -> "API Key" in the 
; right pane.

api_key: 8b5d80c55ddddb00f3445cb9b845b6d

; Issue-URL
;
; Go to your Redmine website and click on an issue. Paste the URL to that issue
; here and substitute the issue's ID with a %d as a placeholder.

issue_url: http://yourhost/redmine/issues/%d.json

; Comment-Added-Template
;
; Whenever as review was done, a note will be added to all the issues that are
; referenced in the change subject and in the cover message of the review. This
; is the template that is used to format the comment. Be sure to begin multi
; line entries with a whitespace or tab on each new line.
;
; Valid placeholders are:
;
;  $comment_author_name
;  $comment_author_email
;  $comment
;  $change_url
;  $change_subject
;  $approvals_verified_value
;  $approvals_review_value
;  $change_owner_name
;  $change_owner_email
;  $change_number
;  $change_project
;  $change_id
;  $change_branch
;  $patchset_uploader_name
;  $patchset_uploader_email
;  $patchset_revision
;  $patchset_number
;  $patchset_ref
;  $patchset_created_on 

comment_added_template: $comment_author_name commented on review $change_url: $comment.
 The original change was authored by $change_owner_name.