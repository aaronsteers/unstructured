"""Unit-test suite for dynamic ElementMetadata.

These tests will probably move into test_elements.py once we like the implementation.
"""

import sys

import pytest

from unstructured.documents.tmp_elements import ElementMetadata


class DescribeElementMetadata:
    """Unit-test suite for `unstructured.documents.elements.ElementMetadata`."""

    # -- It is as small as possible, only storing fields that have a non-None value. --

    # -- The size value is naively computed but gives some sense of the growth dynamics.
    # -- Size is non-deterministic so ranges are used.

    def it_is_small_when_empty(self):
        meta = ElementMetadata()
        assert sys.getsizeof(meta) == 56
        assert 232 <= sys.getsizeof(meta.__dict__) <= 296

    def and_it_is_still_pretty_small_when_it_has_some_fields_populated(self):
        meta = ElementMetadata(
            category_depth=1,
            file_directory="foo/bar",
            page_number=2,
            text_as_html="<table></table>",
            url="https://google.com",
        )
        assert meta.file_directory == "foo/bar"
        assert meta.url == "https://google.com"
        rough_size = sys.getsizeof(meta.__dict__) + sum(
            sys.getsizeof(v) for v in meta.__dict__.values()
        )
        assert 531 <= rough_size <= 539

    # -- It can be constructed with known keyword arguments. In particular, including a non-known
    # -- keyword argument produces a type-error at development time and raises an exception at
    # -- runtime. This catches typos before they reach production.

    def it_detects_unknown_constructor_args_at_both_development_time_and_runtime(self):
        with pytest.raises(TypeError, match="got an unexpected keyword argument 'file_name'"):
            ElementMetadata(file_name="memo.docx")  # pyright: ignore[reportGeneralTypeIssues]

    # -- It knows the types of its known members so type-checking support is available. --

    def it_knows_the_types_of_its_known_members_so_type_checking_support_is_available(self):
        ElementMetadata(
            category_depth="2",  # pyright: ignore[reportGeneralTypeIssues]
            file_directory=True,  # pyright: ignore[reportGeneralTypeIssues]
            text_as_html=42,  # pyright: ignore[reportGeneralTypeIssues]
        )
        # -- it does not check types at runtime however (choosing to avoid validation overhead) --

    # -- It only stores a field's value when it is not None. --

    def it_returns_the_value_of_an_attribute_it_has(self):
        meta = ElementMetadata(url="https://google.com")
        assert "url" in meta.__dict__
        assert meta.url == "https://google.com"

    def and_it_returns_None_for_a_known_attribute_it_does_not_have(self):
        meta = ElementMetadata()
        assert "url" not in meta.__dict__
        assert meta.url is None

    def but_it_raises_AttributeError_for_an_unknown_attribute_it_does_not_have(self):
        meta = ElementMetadata()
        assert "coefficient" not in meta.__dict__
        with pytest.raises(AttributeError, match="object has no attribute 'coefficient'"):
            meta.coefficient

    def it_stores_a_non_None_field_value_when_assigned(self):
        meta = ElementMetadata()
        assert "file_directory" not in meta.__dict__
        meta.file_directory = "tmp/"
        assert "file_directory" in meta.__dict__
        assert meta.file_directory == "tmp/"

    def it_removes_a_field_when_None_is_assigned_to_it(self):
        meta = ElementMetadata(file_directory="tmp/")
        assert "file_directory" in meta.__dict__
        assert meta.file_directory == "tmp/"

        meta.file_directory = None
        assert "file_directory" not in meta.__dict__
        assert meta.file_directory is None

    # -- It can serialize itself to a dict -------------------------------------------------------

    def it_can_serialize_itself_to_a_dict(self):
        meta = ElementMetadata(
            category_depth=1,
            file_directory="tmp/",
            page_number=2,
            text_as_html="<table></table>",
            url="https://google.com",
        )
        assert meta.to_dict() == {
            "category_depth": 1,
            "file_directory": "tmp/",
            "page_number": 2,
            "text_as_html": "<table></table>",
            "url": "https://google.com",
        }

    # -- It allows downstream users to add an arbitrary new member by assignment. ----------------

    def it_allows_an_end_user_to_add_an_arbitrary_field(self):
        meta = ElementMetadata()
        meta.foobar = 7
        assert "foobar" in meta.__dict__
        assert meta.foobar == 7

    def and_fields_so_added_appear_in_the_metadata_JSON(self):
        meta = ElementMetadata()
        meta.foobar = 7
        assert meta.to_dict() == {"foobar": 7}

    def and_it_removes_an_end_user_field_when_it_is_assigned_None(self):
        meta = ElementMetadata()
        meta.foobar = 7
        assert "foobar" in meta.__dict__
        meta.foobar = None
        assert "foobar" not in meta.__dict__
        with pytest.raises(
            AttributeError, match="'ElementMetadata' object has no attribute 'foobar'"
        ):
            meta.foobar

    # -- It can update itself from another instance ----------------------------------------------

    def it_can_update_itself_from_another_instance(self):
        meta = ElementMetadata(category_depth=1, page_number=1)
        meta.coefficient = 0.58
        meta.stem_length = 18
        other = ElementMetadata(file_directory="tmp/", page_number=2)
        other.quotient = 1.4
        other.stem_length = 20

        meta.update(other)

        # -- known-fields present on self but not other are unchanged --
        assert meta.category_depth == 1
        # -- known-fields present on other but not self are added --
        assert meta.file_directory == "tmp/"
        # -- known-fields present on both self and other are updated --
        assert meta.page_number == 2
        # -- ad-hoc-fields present on self but not other are unchanged --
        assert meta.coefficient == 0.58
        # -- ad-hoc-fields present on other but not self are added --
        assert meta.quotient == 1.4
        # -- ad-hoc-fields present on both self and other are updated --
        assert meta.stem_length == 20
        # -- other is left unchanged --
        assert other.category_depth is None
        assert other.file_directory == "tmp/"
        assert other.page_number == 2
        assert other.text_as_html is None
        assert other.url is None
        assert other.quotient == 1.4
        assert other.stem_length == 20
        with pytest.raises(AttributeError, match="etadata' object has no attribute 'coefficient'"):
            other.coefficient

    def but_it_raises_on_attempt_to_update_from_a_non_ElementMetadata_object(self):
        meta = ElementMetadata()
        with pytest.raises(ValueError, match=r"ate\(\)' must be an instance of 'ElementMetadata'"):
            meta.update({"coefficient": "0.56"})  # pyright: ignore[reportGeneralTypeIssues]