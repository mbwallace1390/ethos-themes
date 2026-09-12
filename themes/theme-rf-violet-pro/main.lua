-- RF Violet Pro
-- Lightweight RF Pro outline-focus color variant.
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
        key = "RFVio",
        name = "RF Violet Pro",
        roundButtons = false,
        focusStyle = "outline",
        colors = {
            lcd.RGB(0xF4, 0xF7, 0xFB), -- PRIMARY_COLOR
            lcd.RGB(0x25, 0x1C, 0x34), -- SECONDARY_BGCOLOR
            lcd.RGB(0xB1, 0x4C, 0xFF), -- HIGHLIGHT_COLOR
            lcd.RGB(0x18, 0x18, 0x18), -- HIGHLIGHT_CONTRASTING_COLOR
            lcd.RGB(0x68, 0x74, 0x86), -- DISABLE_COLOR
            lcd.RGB(0x18, 0x10, 0x22), -- PRIMARY_BGCOLOR
            COLOR_BLACK,               -- OVERLAY_COLOR
            lcd.RGB(0xB7, 0xC5, 0xD8), -- SECONDARY_COLOR
            lcd.RGB(0x42, 0xE6, 0x8A), -- SAFE_COLOR
            lcd.RGB(0x0D, 0x08, 0x14), -- PAGE_BGCOLOR
            lcd.RGB(0xFF, 0x5A, 0x5F), -- ERROR_COLOR
            lcd.RGB(0xB6, 0x58, 0xFF), -- ACTIVE_COLOR
            lcd.RGB(0x91, 0x80, 0xA4), -- INACTIVE_COLOR
            lcd.RGB(0xB1, 0x4C, 0xFF), -- BUTTON_BORDER_ACTIVE_COLOR
            lcd.RGB(0x4A, 0x36, 0x60), -- BUTTON_BORDER_COLOR
            lcd.RGB(0xFF, 0xC8, 0x57), -- WARNING_COLOR
            lcd.RGB(0x08, 0x11, 0x0D), -- SAFE_CONTRASTING_COLOR
            lcd.RGB(0x0D, 0x08, 0x14), -- TOPLCD_BGCOLOR (XE/S)
        },
        toolbarBackground = loadToolbar("toolbar-rf-violet-pro.png", "toolbar-rf-violet-pro-x18.png"),
    })
end

return {
    init = init
}
