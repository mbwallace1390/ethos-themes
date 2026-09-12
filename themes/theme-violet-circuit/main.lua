-- Violet Circuit
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
        key = "VioCkt",
        name = "Violet Circuit",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF5, 0xF7, 0xFA), -- PRIMARY_COLOR
            lcd.RGB(0x24, 0x1A, 0x2E), -- SECONDARY_BGCOLOR
            lcd.RGB(0xA8, 0x55, 0xF7), -- HIGHLIGHT_COLOR
            lcd.RGB(0x0F, 0x09, 0x14), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x6A, 0x67, 0x70), -- DISABLE_COLOR
            lcd.RGB(0x17, 0x10, 0x1F), -- PRIMARY_BGCOLOR
            COLOR_BLACK, -- OVERLAY_COLOR
            lcd.RGB(0xD0, 0xA9, 0xF9), -- SECONDARY_COLOR
            lcd.RGB(0x4E, 0xEF, 0x84), -- SAFE_COLOR
            lcd.RGB(0x0C, 0x08, 0x11), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x48, 0x4D), -- ERROR_COLOR
            lcd.RGB(0x00, 0xD4, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x87, 0x84, 0x8D), -- INACTIVE_COLOR
            lcd.RGB(0x00, 0xD4, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4A, 0x45, 0x51), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC7, 0x44), -- WARNING_COLOR
            lcd.RGB(0x07, 0x18, 0x0C), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0C, 0x08, 0x11), -- TOPLCD_BGCOLOR
        },
        toolbarBackground = loadToolbar("toolbar-violet-circuit.png", "toolbar-violet-circuit-x18.png"),
    })
end

return { init = init }
