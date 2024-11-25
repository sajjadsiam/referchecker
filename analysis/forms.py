from django import forms

class TokenDataForm(forms.Form):
    token_data = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',  # Bootstrap or custom class
                'placeholder': (
                    "Paste the main wallet data here...\n"
                    "Example:\n"
                    "0x7c...2Aae 20UXUY\n"
                    "0x01...0E71 20UXUY\n"
                    "0x1c...C296 0UXUY\n"
                    "..."
                ),
                'rows': 8,
                'style': 'resize: none; background-color: #f8f9fa; padding: 10px; '
                         'border: 1px solid #ced4da; border-radius: 5px;'
            }
        ),
        label='Main Wallet Data'
    )

class WalletDataForm(forms.Form):
    wallet_data = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-control',  # Bootstrap or custom class
                'placeholder': (
                    "Paste the referral wallet addresses here...\n"
                    "Example:\n"
                    "0xA9bD1C72Ba2b1e9DfA7F5A2503C11f6522AF02C5\n"
                    "0xc54eFd54D0C68A0de9BAa24B9AA834cAB84D107e\n"
                    "..."
                ),
                'rows': 8,
                'style': 'resize: none; background-color: #f8f9fa; padding: 10px; '
                         'border: 1px solid #ced4da; border-radius: 5px;'
            }
        ),
        label='Refer Wallet Address'
    )
