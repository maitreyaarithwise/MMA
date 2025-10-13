-- =========================================================
--  USERS: Traders and admins who use the dashboard
-- =========================================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique identifier for each user
    username TEXT NOT NULL UNIQUE,                          -- Login/display name, must be unique
    email TEXT UNIQUE,                                      -- Optional contact email
    password_hash TEXT NOT NULL,                            -- Hashed password for login security
    role TEXT CHECK (role IN ('admin','trader')) DEFAULT 'trader', -- Permissions: admin or trader
    kalshi_api_key_encrypted TEXT,                                    -- Primary per-user API key for Kalshi (encrypted in app)
    created_at TIMESTAMPTZ DEFAULT now(),                   -- Timestamp when user was created
    last_login TIMESTAMPTZ                                  -- Last login time for auditing purposes
);
-- Example:
-- ('john', 'john@example.com', 'hashed_pwd1', 'trader', 'encrypted_key1')


-- =========================================================
--  PLATFORMS: Store info for each betting platform
-- =========================================================
CREATE TABLE platforms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique ID per platform
    name TEXT NOT NULL UNIQUE,                              -- Platform name, e.g., 'Kalshi', 'Pinnacle'
    base_url TEXT NOT NULL,                                 -- API base URL for live interaction
    rate_limit_per_min INT,                                 -- Max requests allowed per minute to avoid bans
    account_id_encrypted TEXT,                             -- Account ID (encrypted)
    created_at TIMESTAMPTZ DEFAULT now()                    -- Record creation timestamp
);
-- Example:
-- ('Pinnacle', 'https://api.pinnacle.com', 60, 'encrypted_acc1')
-- ('Kalshi', 'https://api.kalshi.com', 30, 'encrypted_acc2')


-- =========================================================
--  MARKETS: Minimal metadata for live NFL markets
-- =========================================================
CREATE TABLE markets (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique market record ID
    platform_id UUID REFERENCES platforms(id) ON DELETE CASCADE, -- Which platform this market belongs to
    market_id TEXT NOT NULL,                                -- Platform-specific market ID (from API)
    sport TEXT DEFAULT 'NFL',                               -- Sport type (fixed to NFL)
    market_name TEXT,                                       -- Market type: 'Point Spread', 'Moneyline', etc.
    event_name TEXT,                                        -- Event description: 'Patriots vs Chiefs'
    created_at TIMESTAMPTZ DEFAULT now(),                    -- Timestamp of when the market was recorded locally
    UNIQUE(platform_id, market_id)                         -- Unique constraint on platform and market ID
);
-- Example:
-- ('uuid_pinnacle', 'NFL_001', 'NFL', 'Point Spread', 'Patriots vs Chiefs')


-- =========================================================
--  QUOTE ACTIONS LOG: Track every create/update/delete
-- =========================================================
CREATE TABLE quote_actions_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique log entry
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,  -- Which trader triggered the action
    platform_id UUID REFERENCES platforms(id),             -- Platform where action occurred
    market_id TEXT NOT NULL,                                -- Market ID related to the quote
    action_type TEXT CHECK (action_type IN ('CREATE','UPDATE','DELETE')), -- Type of action
    quote_id TEXT,                                         -- Quote/order ID returned by platform API
    payload JSONB,                                        -- Exact request sent to API
    response_status INT,                                  -- HTTP status or API response code
    created_at TIMESTAMPTZ DEFAULT now()                  -- Timestamp of action
);
-- Example:
-- ('uuid_john', 'uuid_kalshi', 'NFL_001', 'CREATE', 'QUOTE_123', '{"odds":1.95,"size":100}', 200)


-- =========================================================
--  PINNACLE CACHE: Temporary odds cache for live comparison
-- =========================================================
CREATE TABLE pinnacle_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique cache record
    event_id TEXT NOT NULL,                                 -- Pinnacle event ID for live comparison
    market_name TEXT NOT NULL,                              -- Market type: 'Spread', 'Moneyline', etc.
    team_name TEXT,                                         -- Side or team name
    odds NUMERIC(10,4),                                     -- Current odds
    spread_width NUMERIC(10,4),                             -- Spread width, used for automation decisions
    last_updated TIMESTAMPTZ DEFAULT now(),                  -- When this cache entry was last refreshed
    UNIQUE(event_id, market_name, team_name)                -- Unique constraint on event, market, and team name
);
-- Example:
-- ('NFL_001', 'Point Spread', 'Patriots', 1.90, 2.5)
-- ('NFL_001', 'Point Spread', 'Chiefs', 1.95, 2.5)


-- =========================================================
--  SYSTEM LOGS: Generic technical/error logs
-- =========================================================
CREATE TABLE system_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique log entry
    level TEXT CHECK (level IN ('info','warn','error')) NOT NULL, -- Severity of log
    message TEXT NOT NULL,                                  -- Short human-readable message
    context JSONB,                                         -- Optional extra data (API response, stack trace)
    timestamp TIMESTAMPTZ DEFAULT now()                    -- When log was created
);
-- Example:
-- ('info', 'Automation rule executed', '{"rule_id":"RULE_001","user":"trader_john"}')
-- ('error', 'Failed to post quote', '{"platform":"Kalshi","quote_id":"QUOTE_123"}')


-- =========================================================
--  AUTOMATION RULES: Auto-trading conditions per trader
-- =========================================================
CREATE TABLE automation_rules (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique rule ID
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,   -- Owner/trader of this rule
    rule_name TEXT NOT NULL,                               -- Descriptive rule name
    trigger_condition JSONB NOT NULL,                      -- JSON logic: when to trigger action (e.g., spread <= 22)
    adjustment_percent NUMERIC(5,2) DEFAULT 0.0,          -- % adjustment applied after fills
    enabled BOOLEAN DEFAULT TRUE,                           -- Whether rule is active
    created_at TIMESTAMPTZ DEFAULT now()                   -- Timestamp of rule creation
);
-- Example:
-- ('uuid_john', 'Spread <= 2.5', '{"spread_width":{"lte":2.5}}', 1.5)


-- =========================================================
--  RISK LIMITS: Exposure and stop-loss rules per trader/platform
-- =========================================================
CREATE TABLE risk_limits (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique risk limit record
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,   -- Trader this applies to
    platform_id UUID REFERENCES platforms(id),             -- Platform reference
    market_id TEXT,                                        -- Market ID (optional)
    limit_type TEXT CHECK (limit_type IN ('position','stop_loss','quote_size')), -- Type of limit
    limit_value NUMERIC(18,2) NOT NULL,                   -- Threshold for risk/stop-loss/position
    active BOOLEAN DEFAULT TRUE,                           -- Whether limit is currently enforced
    created_at TIMESTAMPTZ DEFAULT now(),                   -- Timestamp of record
    UNIQUE(user_id, platform_id, market_id, limit_type)    -- Unique constraint on user, platform, market, and limit type
);
-- Example:
-- ('uuid_john', 'uuid_kalshi', NULL, 'stop_loss', 500)
-- ('uuid_john', 'uuid_kalshi', NULL, 'position', 1000)


-- =========================================================
--  TRADES: Each fill/execution per trader
-- =========================================================
CREATE TABLE trades (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique trade ID
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,   -- Trader who executed the trade
    platform_id UUID REFERENCES platforms(id),             -- Platform where trade occurred
    market_id TEXT NOT NULL,                                -- Market reference
    quote_id TEXT,                                         -- Quote/order ID that produced the fill
    side TEXT CHECK (side IN ('buy','sell')) NOT NULL,     -- Buy or sell side
    price NUMERIC(18,4) NOT NULL,                          -- Execution price
    size NUMERIC(18,4) NOT NULL,                           -- Quantity traded
    counterparty TEXT,                                     -- Optional counterparty info if available
    timestamp TIMESTAMPTZ DEFAULT now(),                    -- Execution time
    UNIQUE(platform_id, market_id, quote_id)              -- Unique constraint on platform, market, and quote ID
);
-- Example:
-- ('uuid_john', 'uuid_kalshi', 'NFL_001', 'QUOTE_123', 'buy', 1.95, 100, 'sharp_bettor_001')


-- =========================================================
--  PNL HISTORY: Profit & Loss snapshots
-- =========================================================
CREATE TABLE pnl_history (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique record ID
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,   -- Trader owner
    platform_id UUID REFERENCES platforms(id),             -- Platform reference
    market_id TEXT,                                        -- Market ID
    realized_pnl NUMERIC(18,4) DEFAULT 0,                 -- Closed trade profit/loss
    unrealized_pnl NUMERIC(18,4) DEFAULT 0,               -- Open position P&L
    total_pnl NUMERIC(18,4) GENERATED ALWAYS AS (realized_pnl + unrealized_pnl) STORED, -- Auto-calculated
    recorded_at TIMESTAMPTZ DEFAULT now(),                  -- Snapshot timestamp
    UNIQUE(user_id, platform_id, market_id, recorded_at)  -- Unique constraint on user, platform, market, and recorded at timestamp
);
-- Example:
-- ('uuid_john', 'uuid_kalshi', 'NFL_001', 50.00, -10.00, 40.00)


-- =========================================================
--  COUNTERPARTY STATS: Track sharp bettors per platform
-- =========================================================
CREATE TABLE counterparty_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique record
    platform_id UUID REFERENCES platforms(id),             -- Platform reference
    counterparty_id TEXT NOT NULL,                         -- Bettor ID/alias
    trades_count INT DEFAULT 0,                             -- Number of trades sampled
    cumulative_pnl NUMERIC(18,4) DEFAULT 0,               -- Total P&L vs this counterparty
    sharp_flag BOOLEAN DEFAULT FALSE,                     -- True if flagged as sharp (>100 trades + profit)
    last_updated TIMESTAMPTZ DEFAULT now(),                 -- Last update timestamp
    UNIQUE(platform_id, counterparty_id)                  -- Unique constraint on platform and counterparty ID
);
-- Example:
-- ('uuid_kalshi', 'sharp_bettor_001', 120, 5000.00, TRUE)


-- =========================================================
--  NOTIFICATIONS: Alerts to users
-- =========================================================
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),          -- Unique notification ID
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,   -- Recipient user
    type TEXT CHECK (type IN ('fill','timeout','error','system')), -- Notification type
    message TEXT NOT NULL,                                  -- Alert text
    read BOOLEAN DEFAULT FALSE,                              -- Has the user read this notification
    created_at TIMESTAMPTZ DEFAULT now()                   -- Timestamp of notification creation
);
-- Example:
-- ('uuid_trader_john', 'fill', 'Your buy order for Patriots vs Chiefs executed', FALSE)
-- ('uuid_trader_john', 'error', 'Failed to post quote on Kalshi', FALSE)
