-- Titanium
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
        key = "Titani",
        name = "Titanium",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x41, 0x48, 0x4F), -- SECONDARY_BGCOLOR
            lcd.RGB(0xC8, 0xD2, 0xDC), -- HIGHLIGHT_COLOR
            lcd.RGB(0x12, 0x16, 0x1A), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x8F, 0x93, 0x98), -- DISABLE_COLOR
            lcd.RGB(0x2F, 0x35, 0x3B), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xE0, 0xE6, 0xEC), -- SECONDARY_COLOR
            lcd.RGB(0x3F, 0xEB, 0x7F), -- SAFE_COLOR
            lcd.RGB(0x1F, 0x24, 0x29), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x44, 0x4D), -- ERROR_COLOR
            lcd.RGB(0xC8, 0xD2, 0xDC), -- ACTIVE_COLOR
            lcd.RGB(0xB2, 0xB5, 0xB8), -- INACTIVE_COLOR
            lcd.RGB(0xCC, 0xD6, 0xDF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x5B, 0x60, 0x65), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x38), -- WARNING_COLOR
            lcd.RGB(0x05, 0x16, 0x0A), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1F, 0x24, 0x29), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-titanium.png", "toolbar-titanium-x18.png"),
    })
end

return { init = init }
