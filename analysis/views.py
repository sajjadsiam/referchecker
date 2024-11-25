import pandas as pd
from django.shortcuts import render
from .forms import TokenDataForm, WalletDataForm

def trim_address(address):
    """Trims an Ethereum address to the format: first 4 chars + ... + last 4 chars."""
    return f"{address[:4]}...{address[-4:]}" if len(address) > 8 else address

def transform_pairs(raw_text):
    """
    Transforms raw token data into pairs of addresses and tokens.
    Each pair associates an Ethereum address with a token (e.g., "0x...:20UXUY").
    """
    lines = raw_text.strip().split("\n")
    pairs = []
    current_address = None

    for line in lines:
        clean_line = line.strip()
        if clean_line.startswith("0x"):  # Ethereum address detected
            current_address = clean_line
        elif clean_line in ["20UXUY", "0UXUY"] and current_address:  # Valid token detected
            pairs.append((current_address, clean_line))
    return pairs

def analyze_wallets(request):
    """
    Analyzes the wallet addresses to check if they contain 20UXUY tokens.
    """
    token_form = TokenDataForm()
    wallet_form = WalletDataForm()
    results = []
    valid_count = 0
    not_valid_count = 0

    if request.method == "POST":
        token_form = TokenDataForm(request.POST)
        wallet_form = WalletDataForm(request.POST)

        if token_form.is_valid() and wallet_form.is_valid():
            # Get data from forms
            token_data = token_form.cleaned_data["token_data"]
            wallet_data = wallet_form.cleaned_data["wallet_data"]

            # Transform token data
            token_pairs = transform_pairs(token_data)
            token_df = pd.DataFrame(token_pairs, columns=["Address", "Token"])

            # Normalize and clean the token DataFrame
            token_df["Address"] = token_df["Address"].str.strip()
            token_df["Token"] = token_df["Token"].str.strip()

            # Process wallet addresses
            wallet_addresses = [address.strip() for address in wallet_data.strip().split("\n")]

            # Analyze wallet addresses
            for address in wallet_addresses:
                trimmed = trim_address(address)

                # Check for exact match first
                matched_row = token_df[token_df["Address"] == address]
                if not matched_row.empty:
                    token = matched_row["Token"].values[0]
                    if token == "20UXUY":
                        results.append({"address": trimmed, "status": "Valid"})
                        valid_count += 1
                    else:
                        results.append({"address": trimmed, "status": "Not Valid"})
                        not_valid_count += 1
                else:
                    # Check if trimmed version matches any token address
                    matched_trimmed_row = token_df[token_df["Address"].apply(lambda x: trim_address(x) == trimmed)]
                    if not matched_trimmed_row.empty:
                        token = matched_trimmed_row["Token"].values[0]
                        if token == "20UXUY":
                            results.append({"address": trimmed, "status": "20UXUY"})
                            valid_count += 1
                        else:
                            results.append({"address": trimmed, "status": "0UXUY"})
                            not_valid_count += 1
                    else:
                        results.append({"address": trimmed, "status": "0UXUY"})
                        not_valid_count += 1

    context = {
        "token_form": token_form,
        "wallet_form": wallet_form,
        "results": results,
        "valid_count": valid_count,
        "not_valid_count": not_valid_count,
    }

    return render(request, "analysis/results.html", context)
