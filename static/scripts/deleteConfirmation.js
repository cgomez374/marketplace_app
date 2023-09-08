/**
This script will ask the user to confirm their decision to
delete their account
**/

const delete_decision = () => {
    if (confirm('Are you sure?')) {
        window.location.href = "{{ url_for('merchant_delete') }}"
    }
}