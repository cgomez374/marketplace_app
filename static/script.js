function delete_decision() {
        if (!confirm('Please confirm you want to delete this account')) {
            console.log('not deleting')
            window.location.href = "{{ url_for('account') }}"
        }
        else {
            window.location.href = "{{ url_for('merchant_delete') }}"
        }
    }