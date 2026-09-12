-- Racing Division
-- Standalone ETHOS radio theme. Rotorflight and RF Suite files are not modified.
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
        key = "RaceDiv",
        name = "Racing Division",
        roundButtons = false,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF5, 0xF5, 0xF5), -- PRIMARY_COLOR
            lcd.RGB(0x29, 0x29, 0x29), -- SECONDARY_BGCOLOR
            lcd.RGB(0xE7, 0x33, 0x33), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0E, 0x0E, 0x0E), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x77, 0x77, 0x77), -- DISABLE_COLOR
            lcd.RGB(0x19, 0x19, 0x19), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD7, 0xD7, 0xD7), -- SECONDARY_COLOR
            lcd.RGB(0x58, 0xD8, 0x89), -- SAFE_COLOR
            lcd.RGB(0x0B, 0x0B, 0x0B), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x3B, 0x3B), -- ERROR_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x90, 0x90, 0x90), -- INACTIVE_COLOR
            lcd.RGB(0xFF, 0xFF, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4A, 0x4A, 0x4A), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC5, 0x4A), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0B, 0x0B, 0x0B), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-racing-division.png", "toolbar-racing-division-x18.png"),
    })
end

return { init = init }
