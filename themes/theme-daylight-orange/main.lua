-- Daylight Orange
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
        key = "DayOrg",
        name = "Daylight Orange",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0x12, 0x18, 0x1E), -- PRIMARY_COLOR
            lcd.RGB(0xE8, 0xE1, 0xDB), -- SECONDARY_BGCOLOR
            lcd.RGB(0xE8, 0x6E, 0x00), -- HIGHLIGHT_COLOR
            lcd.RGB(0x2A, 0x2B, 0x2B), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x7B, 0x82, 0x89), -- DISABLE_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0x46, 0x46, 0x46), -- SECONDARY_COLOR
            lcd.RGB(0x14, 0x91, 0x50), -- SAFE_COLOR
            lcd.RGB(0xF5, 0xF2, 0xF1), -- PAGE_BGCOLOR
            lcd.RGB(0xCC, 0x28, 0x32), -- ERROR_COLOR
            lcd.RGB(0xA2, 0x4D, 0x00), -- ACTIVE_COLOR
            lcd.RGB(0x5A, 0x66, 0x72), -- INACTIVE_COLOR
            lcd.RGB(0xE8, 0x6E, 0x00), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0xBF, 0xBD, 0xBC), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xBE, 0x73, 0x00), -- WARNING_COLOR
            lcd.RGB(0x15, 0x15, 0x16), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0xF5, 0xF2, 0xF1), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-daylight-orange.png", "toolbar-daylight-orange-x18.png"),
    })
end

return { init = init }
