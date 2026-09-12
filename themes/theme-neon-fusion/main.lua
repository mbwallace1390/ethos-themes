-- Neon Fusion
-- Lightweight standalone ETHOS theme.
local function selectToolbar(largeFile, smallFile)
    local version = system.getVersion()
    if version and type(version.lcdWidth) == "number" and version.lcdWidth <= 480 then
        return smallFile
    end
    return largeFile
end

local function loadToolbar(largeFile, smallFile)
    -- Optional artwork must not prevent registration when it cannot be loaded.
    local ok, bitmap = pcall(lcd.loadBitmap, selectToolbar(largeFile, smallFile))
    if ok and bitmap then
        return bitmap
    end
    return nil
end

local function init()
    -- Skip unsupported firmware before creating colors or loading artwork.
    if type(system.registerTheme) ~= "function" then return end
    system.registerTheme({
        key = "NeoFus",
        name = "Neon Fusion",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x1A, 0x2B, 0x2E), -- SECONDARY_BGCOLOR
            lcd.RGB(0x00, 0xD7, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x09, 0x13, 0x14), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6B, 0x72, 0x75), -- DISABLE_COLOR
            lcd.RGB(0x10, 0x1C, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x7F, 0xE8, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x08, 0x0F, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xFF, 0x3E, 0xA5), -- ACTIVE_COLOR
            lcd.RGB(0x89, 0x90, 0x92), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0x3E, 0xA5), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x45, 0x4E, 0x51), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x08, 0x0F, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-neon-fusion.png", "toolbar-neon-fusion-x18.png"),
    })
end

return { init = init }
