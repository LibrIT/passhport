#!/bin/bash
# Remove crashed sessions
wget --no-check-certificate -qO - https://localhost:5000/connection/ssh/checkandterminate
