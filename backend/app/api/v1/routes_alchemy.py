# Removed in v1. The /alchemy/run endpoint has been replaced by /critique/stream.
# See app/api/v1/routes_critique.py
raise ImportError(
    "routes_alchemy is deprecated and should not be imported. Use routes_critique."
)
