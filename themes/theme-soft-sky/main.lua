-- Soft Sky
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
        key = "SSky",
        name = "Soft Sky",
        roundButtons = true,
        focusStyle = "invert",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x34, 0x3E, 0x45), -- SECONDARY_BGCOLOR
            lcd.RGB(0x8F, 0xD3, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x1B, 0x23, 0x29), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x82, 0x87, 0x8B), -- DISABLE_COLOR
            lcd.RGB(0x26, 0x2E, 0x33), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xC2, 0xE5, 0xFC), -- SECONDARY_COLOR
            lcd.RGB(0x8C, 0xE7, 0xB4), -- SAFE_COLOR
            lcd.RGB(0x1A, 0x20, 0x24), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x75, 0x80), -- ERROR_COLOR
            lcd.RGB(0x8F, 0xD3, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0xA3, 0xA7, 0xAA), -- INACTIVE_COLOR
            lcd.RGB(0xA3, 0xDA, 0xFE), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x5E, 0x64, 0x69), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xD0, 0x75), -- WARNING_COLOR
            lcd.RGB(0x14, 0x2A, 0x1E), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x1A, 0x20, 0x24), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-soft-sky.png", "toolbar-soft-sky-x18.png"),
    })
end

return { init = init }
